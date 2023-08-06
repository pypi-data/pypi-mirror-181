# Third-Party
import orjson
from pydantic import BaseModel as PydanticBaseModel  # pylint: disable=no-name-in-module

# Internal
from ehandler.models.utils import orjson_dumps


class BaseModel(PydanticBaseModel):
    """
    Base model with base configuration
    """

    class Config:
        """
        Model Config
        """

        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_assignment = True
        use_enum_values = True
