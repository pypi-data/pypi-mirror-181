from typing import List
from typing import Optional
from typing import Tuple

import pendulum
from pyspark.sql import functions
from pyspark.sql import SparkSession
from pyspark.sql.window import Window

from tecton._internals import data_frame_helper
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.query_consts import ANCHOR_TIME
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_proto.data.feature_store_pb2 import FeatureStoreFormatVersion
from tecton_proto.data.feature_view_pb2 import TrailingTimeWindowAggregation
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.materialization_params import MaterializationParams
from tecton_spark.time_utils import convert_epoch_to_datetime
from tecton_spark.time_utils import convert_epoch_to_timestamp_column

"""
This file contains internal methods of feature_views/aggregations.py
Separate file helps de-clutter the main user-visible file.
"""

_TEMPORAL_PREVIEW_DURATION = pendulum.Duration(days=1)


# This is just plain wrong for bwafv. So anyone trying to use this for feature time limits should be very careful.
def _get_feature_data_time_limits(fd: FeatureDefinition, spine_time_limits):
    if spine_time_limits is None:
        # If there's no spine, it means we need to preview small portion of the dataframe. So we optimize access from
        # the raw data source by applying artificial time limits to the dataframe
        if fd.is_feature_table:
            time_end = pendulum.now()
            # We choose not to subtract by serving_ttl since it shouldn't be
            # vital for preview functionality and it will improve response
            # times.
            time_start = time_end - _TEMPORAL_PREVIEW_DURATION
            return time_start, time_end
        elif fd.is_temporal or fd.is_temporal_aggregate:
            materialization_params = MaterializationParams.from_feature_definition(fd)
            time_end = materialization_params.most_recent_anchor(pendulum.now("UTC"))
            time_start = time_end
            return time_start, time_end
        elif fd.is_on_demand:
            raise ValueError(f"Invalid invocation on OnDemandFeatureView type for: '{fd.name}'")
        else:
            raise ValueError(f"Unknown feature type for: '{fd.name}'")
    else:
        time_start = spine_time_limits.start
        time_end = spine_time_limits.end

        if fd.is_temporal:
            # Subtract by `serving_ttl` to accommodate for enough feature data for the feature expiration
            serving_ttl = fd.serving_ttl
            time_start = time_start - serving_ttl

        # Respect feature_start_time if it's set.
        if fd.feature_start_timestamp:
            time_start = max(time_start, fd.feature_start_timestamp)

        return time_start, time_end


def _align_feature_data_time_limits(
    materialization_params: MaterializationParams, time_start, time_end
) -> Tuple[pendulum.DateTime, pendulum.DateTime]:
    version = materialization_params.feature_definition.get_feature_store_format_version

    # TODO(querytree): be more principled in aligning these timestamps
    if materialization_params.feature_definition.is_temporal_aggregate:
        time_start = materialization_params.most_recent_tile_end_time(time_start)
    else:
        time_start = materialization_params.align_timestamp_left(time_start)
    time_start = convert_epoch_to_datetime(time_start, version)
    # Since feature data time interval is open on the right, we need to always strictly align right so that
    # with `batch_schedule = 1h`, time end `04:00:00` will be aligned to `05:00:00`.
    # NOTE: This may be more permissive than 'allowed_upstream_lateness' would allow,
    # but that's okay from a correctness perspective since our as-of join
    # should account for this.
    time_end = convert_epoch_to_datetime(materialization_params.force_align_timestamp_right(time_end), version)
    return time_start, time_end


# This is actually used to return feature data time limits
def _get_raw_data_time_limits(
    fd: FeatureDefinition, time_start: pendulum.DateTime, time_end: pendulum.DateTime
) -> pendulum.Period:
    if fd.is_temporal_aggregate:
        # Account for final aggregation needing aggregation window prior to earliest timestamp
        max_aggregation_window = fd.max_aggregation_window
        time_start = time_start - max_aggregation_window.ToTimedelta()

    return time_end - time_start


# These are actually feature data time limits. To actually get raw data time limits, you'd need
# to use additional information that is on your FilteredSource or other data source inputs.
def _get_time_limits(
    fd: FeatureDefinition,
    spine_df,
    spine_time_limits: Optional[pendulum.Period],
):
    """Get the time limits to set on the partially aggregated dataframe."""
    if spine_time_limits is None and spine_df is not None:
        spine_time_limits = data_frame_helper._get_time_limits_of_dataframe(spine_df, fd.timestamp_key)
    time_start, time_end = _get_feature_data_time_limits(fd, spine_time_limits)
    if time_start is None and time_end is None:
        return None

    if not fd.is_feature_table:
        materialization_params = MaterializationParams.from_feature_definition(fd)
        time_start, time_end = _align_feature_data_time_limits(materialization_params, time_start, time_end)

    return _get_raw_data_time_limits(fd, time_start, time_end)


# TODO(TEC-9494) - deprecate this method, which is just used by the non-querytree read/run apis
def construct_full_tafv_df(
    spark: SparkSession,
    time_aggregation: TrailingTimeWindowAggregation,
    join_keys: List[str],
    feature_store_format_version: FeatureStoreFormatVersion,
    tile_interval: pendulum.Duration,
    all_partial_aggregations_df=None,
    use_materialized_data=True,
):
    """Construct a full time-aggregation data frame from a partial aggregation data frame.

    :param spark: Spark Session
    :param time_aggregation: trailing time window aggregation.
    :param join_keys: join keys to use on the dataframe.
    :param feature_store_format_version: indicates the time precision used by FeatureStore.
    :param tile_interval: Duration of the aggregation tile interval.
    :param fd: Required only if spine_df is provided. The BWAFV/SWAFV object.
    :param spine_df: (Optional) The spine to join against. If present, the returned data frame
        will contain rollups for all (join key, temporal key) combinations that are required
        to compute a full frame from the spine.
    :param all_partial_aggregations_df: (Optional) The full partial
        aggregations data frame to use in place of the a data frame read from the
        materialized parquet tables.
    :param use_materialized_data: (Optional) Use materialized data if materialization is enabled
    :param raw_data_time_limits: (Optional) Spine Time Bounds
    :param wildcard_key_not_in_spine: (Optional) Whether or not the wildcard join_key is present in the spine.
        Defaults to False if spine is not specified or if the FeatureView has no wildcard join_key.
    """
    output_df = _construct_full_tafv_df_with_anchor_time(
        spark,
        time_aggregation,
        join_keys,
        feature_store_format_version,
        tile_interval,
        all_partial_aggregations_df,
        use_materialized_data,
    )
    output_df = output_df.withColumn(
        ANCHOR_TIME,
        convert_epoch_to_timestamp_column(functions.col(ANCHOR_TIME), feature_store_format_version),
    )
    output_df = output_df.withColumnRenamed(ANCHOR_TIME, time_aggregation.time_key)

    return output_df


def _construct_full_tafv_df_with_anchor_time(
    spark: SparkSession,
    time_aggregation: TrailingTimeWindowAggregation,
    join_keys: List[str],
    feature_store_format_version: FeatureStoreFormatVersion,
    tile_interval: pendulum.Duration,
    all_partial_aggregations_df,
    use_materialized_data=True,
):
    # If spine isn't provided, the fake timestamp equals to anchor time + tile_interval, s.t. the output timestamp
    # completely contains the time range of the fully aggregated window. Note, that ideally we would either subtract
    # 1 second from the timestamp, due to tiles having [start, end) format, or convert tiles in (start, end] format.
    # For now, we're not doing 1 due to it being confusing in preview, and not doing 2 due to it requiring more work
    partial_aggregations_df = all_partial_aggregations_df.withColumn(
        ANCHOR_TIME,
        functions.col(ANCHOR_TIME) + convert_timedelta_for_version(tile_interval, feature_store_format_version),
    )

    aggregations = []
    for feature in time_aggregation.features:
        # We do + 1 since RangeBetween is inclusive, and we do not want to include the last row of the
        # previous tile. See https://github.com/tecton-ai/tecton/pull/1110
        window_duration = pendulum.Duration(seconds=feature.window.ToSeconds())
        upper_range = -(convert_timedelta_for_version(window_duration, feature_store_format_version)) + 1
        window_spec = (
            Window.partitionBy(join_keys).orderBy(functions.col(ANCHOR_TIME).asc()).rangeBetween(upper_range, 0)
        )
        aggregation_plan = get_aggregation_plan(
            feature.function, feature.function_params, time_aggregation.is_continuous, time_aggregation.time_key
        )
        names = aggregation_plan.materialized_column_names(feature.input_feature_name)

        agg = aggregation_plan.full_aggregation_transform(names, window_spec)

        filtered_agg = agg
        aggregations.append(filtered_agg.alias(feature.output_feature_name))

    output_df = partial_aggregations_df.select(join_keys + [ANCHOR_TIME] + aggregations)

    return output_df
