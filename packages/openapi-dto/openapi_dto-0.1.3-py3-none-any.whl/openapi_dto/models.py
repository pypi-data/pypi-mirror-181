from dataclasses import dataclass, field
from typing import Dict, Optional, List, Union

from dataclasses_json import config, dataclass_json, Undefined

ValueExample = Union[
    str, int, float, bool, List["ValueExample"], Dict["ValueExample", "ValueExample"]
]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TypeDefinition:
    type: Optional[str] = None
    ref: Optional[str] = field(default=None, metadata=config(field_name="$ref"))
    format: Optional[str] = None
    title: Optional[str] = None
    nullable: bool = False
    items: Optional["TypeDefinition"] = None
    all_of: Optional[List["TypeDefinition"]] = field(
        default=None, metadata=config(field_name="allOf")
    )
    one_of: Optional[List["Schema"]] = field(
        default=None, metadata=config(field_name="oneOf")
    )
    read_only: Optional[bool] = field(
        default=None, metadata=config(field_name="readOnly")
    )
    write_only: Optional[bool] = field(
        default=None, metadata=config(field_name="writeOnly")
    )
    max_length: Optional[int] = field(
        default=None, metadata=config(field_name="maxLength")
    )
    min_items: Optional[int] = field(
        default=None, metadata=config(field_name="minItems")
    )
    max_items: Optional[int] = field(
        default=None, metadata=config(field_name="maxItems")
    )
    maximum: Optional[int] = None
    minimum: Optional[int] = None
    example: Optional[ValueExample] = None
    enum: Optional[List[str]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Schema:
    type: Optional[str] = None
    enum: Optional[List[str]] = None
    properties: Optional[Dict[str, TypeDefinition]] = None
    required: Optional[List[str]] = None
    all_of: Optional[List["Schema"]] = field(
        default=None, metadata=config(field_name="allOf")
    )
    title: Optional[str] = None
    ref: Optional[str] = field(default=None, metadata=config(field_name="$ref"))
