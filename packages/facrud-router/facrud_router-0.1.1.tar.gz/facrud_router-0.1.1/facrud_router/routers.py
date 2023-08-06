from facrud_router.generics import RouterGeneric
from facrud_router.mixins import (
    RetrieveRouterMixin,
    ListRouterMixin,
    DeleteRouterMixin,
    CreateRouterMixin,
    UpdateRouterMixin,
    PartialUpdateRouterMixin
)


class ModelCRUDRouter(
    RouterGeneric,
    RetrieveRouterMixin,
    ListRouterMixin,
    DeleteRouterMixin,
    CreateRouterMixin,
    UpdateRouterMixin,
    PartialUpdateRouterMixin
):
    pass
