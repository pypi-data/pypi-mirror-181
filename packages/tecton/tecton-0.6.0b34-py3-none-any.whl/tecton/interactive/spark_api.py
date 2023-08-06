import tempfile
from datetime import datetime
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd
from pyspark import sql as pyspark_sql
from pyspark.sql import streaming as pyspark_streaming

from tecton import tecton_context
from tecton._internals import errors
from tecton.interactive.data_frame import TectonDataFrame
from tecton.tecton_context import TectonContext
from tecton_core import materialization_context
from tecton_core import specs
from tecton_core.query import builder
from tecton_core.query import nodes
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_spark import data_source_helper
from tecton_spark import schema_derivation_utils
from tecton_spark import spark_schema_wrapper


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: datetime,
    end_time: datetime,
    apply_translator: bool,
) -> TectonDataFrame:
    spark = TectonContext.get_instance()._spark
    if isinstance(data_source.batch_source, specs.SparkBatchSourceSpec):
        if not data_source.batch_source.supports_time_filtering and (start_time or end_time):
            raise errors.DS_INCORRECT_SUPPORTS_TIME_FILTERING

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)

    elif apply_translator:
        timestamp_key = data_source.batch_source.timestamp_field
        if not timestamp_key and (start_time or end_time):
            raise errors.DS_DATAFRAME_NO_TIMESTAMP

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)
    else:
        if start_time is not None or end_time is not None:
            raise errors.DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER

        node = nodes.RawDataSourceScanNode(data_source).as_ref()
        return TectonDataFrame._create(node)


def start_stream_preview(
    data_source: specs.DataSourceSpec,
    table_name: str,
    apply_translator: bool,
    option_overrides: Optional[Dict[str, str]],
) -> pyspark_streaming.StreamingQuery:
    df = get_stream_preview_dataframe(data_source, apply_translator, option_overrides)

    with tempfile.TemporaryDirectory() as d:
        return (
            df.writeStream.format("memory")
            .queryName(table_name)
            .option("checkpointLocation", d)
            .outputMode("append")
            .start()
        )


def get_stream_preview_dataframe(
    data_source: specs.DataSourceSpec, apply_translator: bool, option_overrides: Optional[Dict[str, str]]
) -> pyspark_sql.DataFrame:
    """
    Helper function that allows start_stream_preview() to be unit tested, since we can't easily unit test writing
    to temporary tables.
    """
    spark = tecton_context.TectonContext.get_instance()._spark

    if apply_translator or isinstance(data_source.stream_source, specs.SparkStreamSourceSpec):
        return data_source_helper.get_ds_dataframe(
            spark, data_source, consume_streaming_data_source=True, stream_option_overrides=option_overrides
        )
    else:
        return data_source_helper.get_non_dsf_raw_stream_dataframe(spark, data_source.stream_source, option_overrides)


def derive_batch_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    batch_post_processor: Optional[Callable],
    batch_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    spark = TectonContext.get_instance()._spark
    if ds_args.HasField("hive_ds_config"):
        return schema_derivation_utils.get_hive_table_schema(
            spark=spark,
            table=ds_args.hive_ds_config.table,
            database=ds_args.hive_ds_config.database,
            post_processor=batch_post_processor,
            timestamp_field=ds_args.hive_ds_config.common_args.timestamp_field,
            timestamp_format=ds_args.hive_ds_config.timestamp_format,
        )
    elif ds_args.HasField("spark_batch_config"):
        return schema_derivation_utils.get_batch_data_source_function_schema(
            spark=spark,
            data_source_function=batch_data_source_function,
            supports_time_filtering=ds_args.spark_batch_config.supports_time_filtering,
        )
    elif ds_args.HasField("redshift_ds_config"):
        # TODO(jake)
        return spark_schema_pb2.SparkSchema()
    elif ds_args.HasField("snowflake_ds_config"):
        assert ds_args.snowflake_ds_config.HasField("url"), "url cannot be None"
        assert ds_args.snowflake_ds_config.HasField("database"), "database cannot be None"
        assert ds_args.snowflake_ds_config.HasField("schema"), "schema cannot be None"
        assert ds_args.snowflake_ds_config.HasField("warehouse"), "warehouse cannot be None"

        return schema_derivation_utils.get_snowflake_schema(
            spark=spark,
            url=ds_args.snowflake_ds_config.url,
            database=ds_args.snowflake_ds_config.database,
            schema=ds_args.snowflake_ds_config.schema,
            warehouse=ds_args.snowflake_ds_config.warehouse,
            role=ds_args.snowflake_ds_config.role if ds_args.snowflake_ds_config.HasField("role") else None,
            table=ds_args.snowflake_ds_config.table if ds_args.snowflake_ds_config.HasField("table") else None,
            query=ds_args.snowflake_ds_config.query if ds_args.snowflake_ds_config.HasField("query") else None,
            post_processor=batch_post_processor,
        )
    elif ds_args.HasField("file_ds_config"):
        schema_override = None
        if ds_args.file_ds_config.HasField("schema_override"):
            schema_override = spark_schema_wrapper.SparkSchemaWrapper.from_proto(ds_args.file_ds_config.schema_override)

        schema_uri = ds_args.file_ds_config.schema_uri if ds_args.file_ds_config.HasField("schema_uri") else None
        timestamp_column = (
            ds_args.file_ds_config.common_args.timestamp_field
            if ds_args.file_ds_config.common_args.HasField("timestamp_field")
            else None
        )
        timestamp_format = (
            ds_args.file_ds_config.timestamp_format if ds_args.file_ds_config.HasField("timestamp_format") else None
        )

        return schema_derivation_utils.get_file_source_schema(
            spark=spark,
            file_format=ds_args.file_ds_config.file_format,
            file_uri=ds_args.file_ds_config.uri,
            convert_to_glue=ds_args.file_ds_config.convert_to_glue_format,
            schema_uri=schema_uri,
            schema_override=schema_override,
            post_processor=batch_post_processor,
            timestamp_col=timestamp_column,
            timestmap_format=timestamp_format,
        )
    else:
        raise ValueError(f"Invalid batch source args: {ds_args}")


def derive_stream_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    stream_post_processor: Optional[Callable],
    stream_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    spark = TectonContext.get_instance()._spark
    if ds_args.HasField("kinesis_ds_config"):
        return schema_derivation_utils.get_kinesis_schema(
            spark, ds_args.kinesis_ds_config.stream_name, stream_post_processor
        )
    elif ds_args.HasField("kafka_ds_config"):
        return schema_derivation_utils.get_kafka_schema(spark, stream_post_processor)
    elif ds_args.HasField("spark_stream_config"):
        return schema_derivation_utils.get_stream_data_source_function_schema(spark, stream_data_source_function)
    else:
        raise ValueError(f"Invalid stream source args: {ds_args}")


_TRANSFORMATION_RUN_TEMP_VIEW_PREFIX = "_tecton_transformation_run_"
CONST_TYPE = Union[str, int, float, bool]


def run_transformation_mode_spark_sql(
    *inputs: Union[pd.DataFrame, pd.Series, "TectonDataFrame", "pyspark.sql.DataFrame", CONST_TYPE],
    transformer: Callable,
    context: materialization_context.BaseMaterializationContext = None,
    transformation_name: str,
) -> TectonDataFrame:
    def create_temp_view(df, dataframe_index) -> str:
        df = TectonDataFrame._create(df).to_spark()
        temp_view = f"{_TRANSFORMATION_RUN_TEMP_VIEW_PREFIX}{transformation_name}_input_{dataframe_index}"
        df.createOrReplaceTempView(temp_view)
        return temp_view

    args = [create_temp_view(v, i) if not isinstance(v, CONST_TYPE.__args__) else v for i, v in enumerate(inputs)]
    if context is not None:
        args.append(context)

    spark = TectonContext.get_instance()._get_spark()
    return TectonDataFrame._create(spark.sql(transformer(*args)))


def run_transformation_mode_pyspark(
    *inputs: Union[pd.DataFrame, pd.Series, "TectonDataFrame", "pyspark.sql.DataFrame", CONST_TYPE],
    transformer: Callable,
    context: materialization_context.BaseMaterializationContext,
) -> TectonDataFrame:
    args = [TectonDataFrame._create(v).to_spark() if not isinstance(v, CONST_TYPE.__args__) else v for v in inputs]
    if context is not None:
        args.append(context)

    return TectonDataFrame._create(transformer(*args))
