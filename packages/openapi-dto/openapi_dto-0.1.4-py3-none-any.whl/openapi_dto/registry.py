import ast
from typing import Union


class TypeRegistry:
    """
    A container for all the types used in the context of an API. The primitives
    are registered automatically, but custom complex types have to be added
    manually.
    """

    def __init__(self, indent=4):
        self.type_mapping = {
            "integer": int,
            "number": float,
            "string": str,
            "boolean": bool,
            "list": list,
        }
        self.primitives = tuple(self.type_mapping.values())
        self.indent = indent
        self.imports = []

    def map(self, name: str, clazz: ast.AST) -> "TypeRegistry":
        self.type_mapping[name] = clazz
        return self

    def add_import(
        self,
        import_ast: Union[ast.Import, ast.ImportFrom],
    ) -> "TypeRegistry":
        if import_ast not in self.imports:
            self.imports.append(import_ast)
        return self

    def is_primitive(self, type_name: str) -> bool:
        type_ = self.type_mapping.get(type_name)
        return type_ in self.primitives

    def to_source_code(self) -> str:
        code_parts = [
            "\n".join(ast.unparse(import_line) for import_line in self.imports)
        ]
        for name, type_ in self.type_mapping.items():
            if type_ in self.primitives:
                continue
            code_parts.append(ast.unparse(type_))
        return "\n\n\n".join(code_parts)

    def __getitem__(self, item):
        return self.type_mapping.get(item)

    def __len__(self):
        return len(self.type_mapping)

    def __contains__(self, item):
        return item in self.type_mapping
