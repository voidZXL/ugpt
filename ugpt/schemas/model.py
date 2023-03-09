import utype
from utype.types import *


class PermissionObject(utype.Schema):
    __options__ = utype.Options(ignore_required=True)

    allow_create_engine: bool
    allow_fine_tuning: bool
    allow_logprobs: bool
    allow_sampling: bool
    allow_search_indices: bool
    allow_view: bool
    created: datetime
    group: Optional[Any]
    id: str
    is_blocking: bool
    object: str = "model_permission"
    organization: str


class ModelData(utype.Schema):
    created: datetime
    id: str
    root: str
    object: str
    owned_by: str
    parent: Optional[Any]
    permissions: List[PermissionObject]


class ModelListResult(utype.Schema):
    data: List[ModelData]
    object: str = "list"
