import json
import urllib
from pathlib import Path
from typing import Optional, List
from urllib.request import urlretrieve

import ast
import typer
import logging

from openapi_dto.config import NamingConvention, OutputEngine
from openapi_dto.engine.base import BaseDTOEngine
from openapi_dto.engine.dataclasses import DataclassesEngine
from openapi_dto.models import Schema
from openapi_dto.registry import TypeRegistry

logger = logging.getLogger(__name__)

app = typer.Typer()


ENGINE_MAPPING = {
    OutputEngine.DATACLASS: DataclassesEngine,
}


@app.command()
def main(
    openapi_file_path: str,
    naming_convention: NamingConvention = typer.Option(
        NamingConvention.SNAKE_CASE.value,
        case_sensitive=False,
    ),
    output_engine: OutputEngine = typer.Option(
        OutputEngine.DATACLASS.value,
        case_sensitive=False,
    ),
    http_header: Optional[List[str]] = None,
):
    logger.info("Loading OpenAPI schema definition from %s", openapi_file_path)
    logger.info("Using %s as naming convention", naming_convention)
    logger.info("Output engine: %s", output_engine)

    # Process the headers to the format that is expected by urllib
    http_header = (
        [] if http_header is None else list(map(lambda x: x.split(":", 1), http_header))
    )

    # Process both remote and local files
    openapi_schema_path = Path(openapi_file_path)
    if not openapi_schema_path.exists():
        # This is a remote file that has to be downloaded first
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ("Accept", "application/json"),
        ] + http_header
        urllib.request.install_opener(opener)
        tmp_file, _ = urllib.request.urlretrieve(openapi_file_path)
        openapi_schema_path = Path(tmp_file)

    # Load schemas from the provided API definition
    openapi_schema = json.loads(openapi_schema_path.read_text())

    # There might be different ways of encoding the schema, so we try them
    try:
        schemas = openapi_schema["components"]["schemas"]
    except KeyError:
        schemas = openapi_schema["definitions"]

    # Process the types one by one
    registry = TypeRegistry()
    engine: BaseDTOEngine = ENGINE_MAPPING.get(output_engine)(
        type_registry=registry,
        naming_convention=naming_convention,
    )
    for type_name, type_schema in schemas.items():
        schema = Schema.from_dict(type_schema)
        generated_type = engine.generate_type(type_name, schema)
        registry.map(type_name, generated_type)

    # Display the complete source code
    print(registry.to_source_code())
