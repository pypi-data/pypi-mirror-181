# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facrud_router']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.88.0,<0.89.0',
 'pydantic>=1.10.2,<2.0.0',
 'sqlalchemy>=1.4.45,<2.0.0']

setup_kwargs = {
    'name': 'facrud-router',
    'version': '0.1.1',
    'description': 'FastApi CRUD router for SQLAlchemy',
    'long_description': '<p align="center">\n  <a href="https://pypi.org/project/facrud-router" style="font-size: 7vw">facrud-router</a>\n</p>\n<div align="center">\n  <a href="https://pypi.org/project/facrud-router" target="_blank">\n      <img src="https://img.shields.io/pypi/pyversions/facrud-router.svg?color=%2334D058" alt="Supported Python versions">\n  </a>\n</div>\n\n---\n\n**Source Code**: <a href="https://github.com/drtnn/facrud-router" target="_blank">https://github.com/drtnn/facrud-router</a>\n\n---\n\n## Requirements\n\nPython 3.9+\n\nfacrud-router stands on the shoulders of giants:\n\n* <a href="https://fastapi.tiangolo.com/" class="external-link" target="_blank">FastAPI</a>\n* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>\n* <a href="https://docs.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a>\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install facrud-router\n\n---> 100%\n```\n\n</div>\n\n## Example\n\n### Create it\n\n* Create a file `main.py` with:\n\n```Python\nimport uuid\nfrom dataclasses import dataclass\nfrom dataclasses import field\n\nimport uvicorn\nfrom facrud_router import ModelCRUDRouter\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel, Field\nfrom sqlalchemy import Column, String\nfrom sqlalchemy.dialects.postgresql import UUID\n\nfrom app.api.deps import get_session\nfrom app.api.deps import authentication_scheme\n\napp = FastAPI(\n    title="FastAPI CURD Router Demo",\n    version="0.1.1",\n    description="FastAPI CRUD Router for SQLAlchemy",\n    openapi_url="/openapi.json",\n    docs_url="/",\n)\n\n\n@dataclass\nclass User:\n    __sa_dataclass_metadata_key__ = "sa"\n    __tablename__ = "user"\n\n    id: uuid.UUID = field(\n        init=False,\n        default_factory=uuid.uuid4,\n        metadata={"sa": Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)},\n    )\n    username: str = field(metadata={"sa": Column(String(255), nullable=False, index=True)})\n    full_name: str = field(metadata={"sa": Column(String(255), nullable=False)})\n\n\nclass UserRequestSchema(BaseModel):\n    username: str = Field(title="Username", max_length=255)\n    full_name: str = Field(title="User Full Name", max_length=255)\n\n\nclass UserResponseSchema(BaseModel):\n    id: uuid.UUID = Field(title="User Id")\n    username: str = Field(title="Username", max_length=255)\n    full_name: str = Field(title="User Full Name", max_length=255)\n\n\nrouter = ModelCRUDRouter(\n    prefix="user",\n    model=User,\n    identifier_type=uuid.UUID,\n    get_session=get_session,\n    get_authentication=authentication_scheme,\n    request_schema=UserRequestSchema,\n    response_schema=UserResponseSchema\n)\n\napp.include_router(router.api_router)\n\nif __name__ == "__main__":\n    uvicorn.run(app)\n```\n\n### Run it\n\nRun the server with:\n\n<div class="termy">\n\n```console\n$ uvicorn main:app --reload\n\nINFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\nINFO:     Started reloader process [28720]\nINFO:     Started server process [28722]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\n```\n\n</div>\n\n### Check it\n\nYou already created an API that:\n\n* GET `/user/{user_id}` retrieves User object by UUID.\n* GET `/user` returns list of User objects.\n* POST `/user` creates User object.\n* DELETE `/user/{user_id}` deletes User object by UUID.\n* PUT `/user/{user_id}` updates User object by UUID.\n* PATCH `/user/{user_id}` partial updates User object by UUID.\n\n### Interactive API docs\n\nNow go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000</a>.\n\nYou will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):\n\n![Swagger UI](https://s277iva.storage.yandex.net/rdisk/39f77d6a2a593fcede3451e4194b5c1a053d36e5cd19df08aefcb71c86462a16/639a5c01/Mi8za20nmVQrIk4Fir018ergP14R4XLjm1uJKqpk3XOveziTE8zylkfyZXMhjEI8Lo-1k6j_qfSKDKxzgrX-nQ==?uid=0&filename=Снимок%20экрана%202022-12-14%20в%2022.27.48.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&fsize=294734&hid=6c672c8a77ee2319904796e479f32ca5&media_type=image&tknv=v2&etag=6caedc9763924ef4f783c454bacd5280&rtoken=k4U9Mma4C5VY&force_default=no&ycrid=na-ba31b448645bc9c9ebc720e5b053697c-downloader1e&ts=5efd2165e4240&s=6256b791ad3cf37e9e0ad18aafb43cbaaba7fd482ef308966b55d70fbc76d3b6&pb=U2FsdGVkX1_7XtCdPrLpy5WEc4mK7uDBcLcXGBLcy3mWB3nbjWhWx3c_S30YJv8mSie8ZL_Q0AmgK5XH_cesURROSl2UAOBZbp-l_JY77ZE)\n\n## License\n\nThis project is licensed under the terms of the Apache License 2.0.',
    'author': 'arutyunyan',
    'author_email': '8david@inbox.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
