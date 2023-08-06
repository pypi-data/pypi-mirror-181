from typing import Callable

import attrs
from typeguard import typechecked

from tecton_core import function_deserialization
from tecton_core import id_helper
from tecton_core.specs import utils
from tecton_proto.args import new_transformation_pb2 as new_transformation__args_pb2
from tecton_proto.data import new_transformation_pb2 as new_transformation__data_pb2

__all__ = ["TransformationSpec"]


@utils.frozen_strict
class TransformationSpec:
    name: str
    id: str
    transformation_mode: new_transformation__args_pb2.TransformationMode
    user_function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: new_transformation__data_pb2.NewTransformation) -> "TransformationSpec":
        user_function = None
        if proto.HasField("user_function"):
            user_function = function_deserialization.from_proto(proto.user_function)
        return cls(
            name=proto.fco_metadata.name,
            id=id_helper.IdHelper.to_string(proto.transformation_id),
            transformation_mode=proto.transformation_mode,
            user_function=user_function,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: new_transformation__args_pb2.NewTransformationArgs, user_function: Callable
    ) -> "TransformationSpec":
        return cls(
            name=proto.info.name,
            id=id_helper.IdHelper.to_string(proto.transformation_id),
            transformation_mode=proto.transformation_mode,
            user_function=user_function,
        )
