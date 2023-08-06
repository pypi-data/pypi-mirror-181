from enum import Enum


class NamingConvention(Enum):
    SNAKE_CASE = "snake"
    CAMEL_CASE = "camel"


class OutputEngine(Enum):
    DATACLASS = "dataclass"
