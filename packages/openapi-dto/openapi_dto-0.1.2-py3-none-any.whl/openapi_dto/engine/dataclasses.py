import ast

from openapi_dto.config import NamingConvention
from openapi_dto.engine.base import BaseDTOEngine
from openapi_dto.models import TypeDefinition, Schema
from openapi_dto.registry import TypeRegistry


class DataclassesEngine(BaseDTOEngine):
    """
    Engine using Python built-in dataclasses with dataclasses-json to generate
    the DTOs.
    """

    def __init__(
        self, type_registry: TypeRegistry, naming_convention: NamingConvention
    ):
        super().__init__(type_registry, naming_convention)
        self.type_registry.add_import(
            ast.ImportFrom(
                module="dataclasses",
                names=[
                    ast.alias(name="dataclass"),
                    ast.alias(name="field"),
                ],
                level=0,
            )
        )
        self.type_registry.add_import(
            ast.ImportFrom(
                module="typing",
                names=[
                    ast.alias(name="List"),
                    ast.alias(name="Union"),
                    ast.alias(name="Optional"),
                ],
                level=0,
            )
        )

    def generate_type(self, name: str, type_schema: Schema) -> ast.AST:
        if type_schema.enum is not None:
            return self._generate_enum(name, type_schema)
        return self._generate_class(name, type_schema)

    def _generate_class(
        self,
        name: str,
        type_schema: Schema,
    ) -> ast.AST:
        if type_schema.properties is not None:
            class_body = []
            nullable_groups = [
                (
                    False,
                    None,
                ),  # First all the non-nullable fields
                (True,),  # Then the nullable ones
            ]
            for nullable_group in nullable_groups:
                for type_name, type_def in type_schema.properties.items():
                    if type_def.nullable not in nullable_group:
                        continue
                    class_body.append(self._generate_field(name, type_name, type_def))
        else:
            class_body = [ast.Pass()]

        return ast.ClassDef(
            name=name,
            bases=[],
            keywords=[],
            body=class_body,
            decorator_list=[
                ast.Name(
                    id="dataclass",
                    ctx=ast.Load(),
                ),
            ],
        )

    def _generate_field(
        self,
        class_name: str,
        field_name: str,
        type_def: TypeDefinition,
    ) -> ast.AST:
        normalized_field_name = self.convert_name(field_name)
        type_annotation = self._get_field_type_annotation(
            class_name,
            field_name,
            type_def,
        )

        args, keywords = [], []
        if type_def.nullable is True:
            keywords.append(ast.keyword(arg="default", value=ast.Constant(value=None)))
        if field_name != normalized_field_name:
            keywords.append(
                ast.keyword(arg="field_name", value=ast.Constant(value=field_name)),
            )
        value = ast.Call(
            func=ast.Name(id="field", ctx=ast.Load()),
            args=args,
            keywords=keywords,
        )

        return ast.AnnAssign(
            target=ast.Name(id=normalized_field_name, ctx=ast.Store()),
            annotation=type_annotation,
            value=value,
            simple=True,
        )

    def _get_field_type_annotation(
        self,
        class_name: str,
        field_name: str,
        type_def: TypeDefinition,
    ):
        if type_def.ref is not None:
            # If the $ref is provided, it should reference to one of the other
            # types, so we can just use this value.
            field_type_name = type_def.ref.split("/")[-1]
            if field_type_name not in self.type_registry:
                field_type_name = f'"{field_type_name}"'
            type_annotation = ast.Name(id=field_type_name, ctx=ast.Load())
        elif class_name == type_def.type:
            # That means there is a recursive definition, so the original name
            # cannot be used without the quotation marks. This is also not
            # registered yet, so it cannot be derived from the registry.
            field_type_name = f'"{class_name}"'
            type_annotation = ast.Name(id=field_type_name, ctx=ast.Load())
        elif type_def.items is not None:
            # Arrays are defined as Python list of objects with a type derived
            # from the items' definition.
            subfield_type_annotation = self._get_field_type_annotation(
                class_name,
                field_name,
                type_def.items,
            )
            type_annotation = ast.Subscript(
                value=ast.Name(id="List", ctx=ast.Load()),
                slice=subfield_type_annotation,
                ctx=ast.Load(),
            )
        elif type_def.all_of is not None:
            # In some cases there might be multiple types accepted
            subfield_type_annotations = [
                self._get_field_type_annotation(
                    class_name,
                    field_name,
                    item,
                )
                for item in type_def.all_of
            ]
            type_annotation = ast.Subscript(
                value=ast.Name(id="Union", ctx=ast.Load()),
                slice=subfield_type_annotations,
                ctx=ast.Load(),
            )
        elif type_def.one_of is not None:
            auto_types = []
            for i, item in enumerate(type_def.one_of):
                auto_class_name = f"{class_name}_{field_name}_{i}"
                auto_type = self.generate_type(auto_class_name, item)
                self.type_registry.map(auto_class_name, auto_type)
                auto_types.append(ast.Name(id=auto_class_name, ctx=ast.Load()))

            type_annotation = ast.Subscript(
                value=ast.Name(id="Union", ctx=ast.Load()),
                slice=ast.Tuple(elts=auto_types),
                ctx=ast.Load(),
            )
        else:
            field_type_name = self.type_registry[type_def.type].__name__
            type_annotation = ast.Name(id=field_type_name, ctx=ast.Load())

        if type_def.nullable is True:
            # Nullable fields are marked as optional, so they accept None
            type_annotation = ast.Subscript(
                value=ast.Name(id="Optional", ctx=ast.Load()),
                slice=type_annotation,
                ctx=ast.Load(),
            )

        if type_def.enum is not None:
            # TODO: provide choices to field
            pass

        return type_annotation

    def _generate_enum(self, name: str, type_schema: Schema) -> ast.AST:
        self.type_registry.add_import(
            ast.ImportFrom(
                module="enum",
                names=[ast.alias(name="Enum")],
                level=0,
            )
        )

        return ast.ClassDef(
            name=name,
            bases=[ast.Name(id="Enum", ctx=ast.Load())],
            keywords=[],
            body=[
                ast.Assign(
                    targets=[
                        ast.Name(id=value.upper(), ctx=ast.Store()),
                    ],
                    value=ast.Constant(value=value),
                    lineno=0,
                )
                for value in type_schema.enum
            ],
            decorator_list=[],
        )
