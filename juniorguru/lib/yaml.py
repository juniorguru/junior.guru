from datetime import datetime

from strictyaml.scalar import ScalarValidator
from strictyaml import Decimal as BaseDecimal
from strictyaml.ruamel.scalarstring import DoubleQuotedScalarString


class Date(ScalarValidator):
    def validate_scalar(self, chunk):
        return datetime.strptime(chunk.contents, "%Y-%m-%d").date()


class Decimal(BaseDecimal):
    def to_yaml(self, data) -> str:
        return DoubleQuotedScalarString(str(data))
