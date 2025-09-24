from datetime import datetime

from pydantic import BaseModel, ConfigDict
from strictyaml import Decimal as BaseDecimal
from strictyaml.ruamel.scalarstring import DoubleQuotedScalarString
from strictyaml.scalar import ScalarValidator


# Utilities for the new way of doing things: Pydantic + PyYAML


class YAMLConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


# Utilities for the old way of doing things: StrictYAML


class Date(ScalarValidator):
    def validate_scalar(self, chunk):
        return datetime.strptime(chunk.contents, "%Y-%m-%d").date()


class Decimal(BaseDecimal):
    def to_yaml(self, data) -> str:
        return DoubleQuotedScalarString(str(data))
