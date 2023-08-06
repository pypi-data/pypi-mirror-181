# openapi-dto

This small library allows generating Python DTOs from the OpenAPI schema 
definition. By default, it uses dataclasses, but it's open for extensions
and using libraries like pydantic instead.

After installation, it might be called in the following way:

```bash
openapi_dto \
  --naming-convention=camel \
  https://foobar.com/api/schema/
```
