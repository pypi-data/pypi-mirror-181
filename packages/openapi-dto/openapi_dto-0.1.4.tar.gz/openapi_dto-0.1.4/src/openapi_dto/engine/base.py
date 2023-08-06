import abc
import ast

import camel_converter

from openapi_dto.config import NamingConvention
from openapi_dto.models import TypeDefinition
from openapi_dto.registry import TypeRegistry


class BaseDTOEngine(abc.ABC):
    """
    An interface for all the engines producing the output DTOs. The engine is
    responsible for generating all the Data Transfer Objects along with their
    source code.
    """

    def __init__(
        self, type_registry: TypeRegistry, naming_convention: NamingConvention
    ):
        self.type_registry = type_registry
        self.naming_convention = naming_convention
        self.imports = []

    def generate_type(self, name: str, type_def: TypeDefinition) -> ast.AST:
        raise NotImplementedError

    def convert_name(self, name: str) -> str:
        if NamingConvention.SNAKE_CASE == self.naming_convention:
            return camel_converter.to_snake(name)
        if NamingConvention.CAMEL_CASE == self.naming_convention:
            return camel_converter.to_camel(name)
        raise ValueError(
            "Naming convention is incorrect. Has to be any of: "
            "NamingConvention.SNAKE_CASE, NamingConvention.CAMEL_CASE"
        )
