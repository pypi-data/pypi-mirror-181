from typing import Optional
from typing import Tuple

import attrs
from typeguard import typechecked

from tecton_core import id_helper
from tecton_core.specs import utils
from tecton_proto.args import entity_pb2 as entity__args_pb2
from tecton_proto.data import entity_pb2 as entity__data_pb2

__all__ = [
    "EntitySpec",
]


@utils.frozen_strict
class EntitySpec:
    name: str
    id: str
    join_keys: Tuple[str, ...]
    # is_local_object is True if the spec represents an object applied locally, as opposed to applied on the backend.
    is_local_object: bool = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    workspace: Optional[str] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: entity__data_pb2.Entity) -> "EntitySpec":
        return cls(
            name=utils.get_field_or_none(proto.fco_metadata, "name"),
            id=id_helper.IdHelper.to_string(proto.entity_id),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            workspace=utils.get_field_or_none(proto.fco_metadata, "workspace"),
            is_local_object=False,
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: entity__args_pb2.EntityArgs) -> "EntitySpec":
        return cls(
            name=utils.get_field_or_none(proto.info, "name"),
            id=id_helper.IdHelper.to_string(proto.entity_id),
            join_keys=utils.get_tuple_from_repeated_field(proto.join_keys),
            workspace=None,
            is_local_object=True,
        )
