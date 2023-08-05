from typing import Optional

from pydantic import AnyUrl, BaseModel


def snake_to_camel(string: str) -> str:
    """
    Convert snake case string to camel case.

    :param string: input snake case string
    :return: str
    """
    return "".join(
        [
            word.lower() if idx == 0 else word.capitalize()
            for idx, word in enumerate(string.split("_"))
        ]
    )


class SchemaBase(BaseModel):
    class Config:
        alias_generator = snake_to_camel


class Environment(SchemaBase):
    name: str
    api_url: AnyUrl
    stage_order: int


class Organization(SchemaBase):
    name: str
    environments: list[Environment] = []


class Enterprise(SchemaBase):
    name: str
    auth_realm: str
    auth_url: AnyUrl
    organizations: Optional[list[Organization]] = []
    default_environment: Optional[Environment]
