from typing import Any

# Third-Party
import orjson


def orjson_dumps(value: Any, *, default=str) -> str:
    """
    `orjson.dumps` returns bytes, decode to match standard `json.dumps`

    :param value: value to dump send by `pydantic.model.json()`
    :param default: Custom encoder send by pydantic

    :return: str like json

    See Also:
        - https://pydantic-docs.helpmanual.io/usage/exporting_models/#json_encoders
        - https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation
    """
    return orjson.dumps(value, default=default).decode()
