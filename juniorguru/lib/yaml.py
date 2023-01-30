from datetime import datetime

from strictyaml.scalar import ScalarValidator


class Date(ScalarValidator):
    def validate_scalar(self, chunk):
        return datetime.strptime(chunk.contents, '%Y-%m-%d').date()
