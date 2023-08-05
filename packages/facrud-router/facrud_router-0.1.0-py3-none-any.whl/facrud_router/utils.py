from typing import Optional

from pydantic import BaseModel
from pydantic.main import ModelMetaclass


class AllOptionalFields(ModelMetaclass):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(mcs, name, bases, namespaces, **kwargs)


def get_all_optional_fields_model(model: BaseModel.__class__):
    class AllOptionalFieldsModel(model, metaclass=AllOptionalFields):
        pass

    return AllOptionalFieldsModel
