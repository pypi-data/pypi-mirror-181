import uuid
from typing import TypeVar, Callable, Optional, List, AsyncGenerator

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from facrud_router.utils import get_all_optional_fields_model

Model = TypeVar("Model")
Authentication = TypeVar("Authentication")
IdentifierType = TypeVar("IdentifierType", uuid.UUID.__class__, int.__class__, str.__class__)


class RouterGeneric:
    prefix: str

    model: Model
    identifier_type: IdentifierType

    kwargs: dict

    get_session: Callable[[], AsyncGenerator[AsyncSession, None]]
    get_authentication: Callable[[], Optional[Authentication]]

    request_schema: Optional[BaseModel.__class__]
    create_request_schema: Optional[BaseModel.__class__]
    update_request_schema: Optional[BaseModel.__class__]
    partial_update_request_schema: Optional[BaseModel.__class__]

    response_schema: Optional[BaseModel.__class__]
    retrieve_response_schema: Optional[BaseModel.__class__]
    list_response_schema: Optional[BaseModel.__class__]
    create_response_schema: Optional[BaseModel.__class__]
    update_response_schema: Optional[BaseModel.__class__]
    partial_update_response_schema: Optional[BaseModel.__class__]

    api_router: APIRouter

    CRUD_ACTIONS: List[str] = ["retrieve", "list", "delete", "create", "update", "partial_update"]

    def __init__(
            self,
            prefix: str,
            api_router: Optional[APIRouter],
            identifier_type: IdentifierType,
            model: Model,
            get_session: Callable,
            get_authentication: Callable,
            request_schema: Optional[BaseModel.__class__] = None,
            create_request_schema: Optional[BaseModel.__class__] = None,
            update_request_schema: Optional[BaseModel.__class__] = None,
            partial_update_request_schema: Optional[BaseModel.__class__] = None,
            response_schema: Optional[BaseModel.__class__] = None,
            retrieve_response_schema: Optional[BaseModel.__class__] = None,
            list_response_schema: Optional[BaseModel.__class__] = None,
            create_response_schema: Optional[BaseModel.__class__] = None,
            update_response_schema: Optional[BaseModel.__class__] = None,
            partial_update_response_schema: Optional[BaseModel.__class__] = None,
            **kwargs
    ):
        self.prefix = prefix
        self.api_router = api_router if api_router else APIRouter()
        self.model = model
        self.identifier_type = identifier_type
        self.kwargs = kwargs
        self.get_session = get_session
        self.get_authentication = get_authentication

        self.request_schema = request_schema
        self.create_request_schema = request_schema
        self.update_request_schema = request_schema
        self.partial_update_request_schema = get_all_optional_fields_model(request_schema)

        if create_request_schema:
            self.create_request_schema = create_request_schema
        if update_request_schema:
            self.update_request_schema = update_request_schema
        if partial_update_request_schema:
            self.partial_update_request_schema = partial_update_request_schema
        elif update_request_schema:
            self.partial_update_request_schema = get_all_optional_fields_model(update_request_schema)

        self.response_schema = response_schema
        self.retrieve_response_schema = response_schema
        self.list_response_schema = List[response_schema]
        self.create_response_schema = response_schema
        self.update_response_schema = response_schema
        self.partial_update_response_schema = response_schema

        if retrieve_response_schema:
            self.retrieve_response_schema = retrieve_response_schema
        if list_response_schema:
            self.list_response_schema = list_response_schema
        if create_response_schema:
            self.create_response_schema = create_response_schema
        if update_response_schema:
            self.update_response_schema = update_response_schema
        if partial_update_response_schema:
            self.partial_update_response_schema = partial_update_response_schema

        self.__register_actions()

    def __register_actions(self):
        for action in self.CRUD_ACTIONS:
            try:
                register_action = getattr(self, f"register_{action}_action")
            except AttributeError:
                pass
            else:
                register_action()
