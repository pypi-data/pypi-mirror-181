"""Django Fields from marshmallow-dataclass."""
__version__ = "0.4.0"

from typing import Dict, List

from django.db import migrations
from marshmallow import Schema

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField


__all__ = (
    "MarshmallowField",
    "marshmallow_dataclass_djangofield",
)


class MarshmallowField(JSONField):
    def __init__(self, *args, many: bool = False, schema: Schema, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.schema = schema
        self.many = many

    def deconstruct(self, *args, **kwargs):
        name, path, args, kwargs = super().deconstruct()
        kwargs["many"] = self.many
        kwargs["schema"] = self.schema
        return name, path, args, kwargs

    def get_prep_value(self, value):
        return super().get_prep_value(list(map(self.schema.dump, value)))

    def from_db_value(self, value, *args, **kwargs):
        if hasattr(super(), "from_db_value"):  # Django v >=3.1
            suped = super().from_db_value(value, *args, **kwargs)
        else:  # Django v <3.1
            suped = super().to_python(value)

        if self.many:
            return list(map(self.schema.load, suped))
        return self.schema.load(suped)


def marshmallow_dataclass_djangofield(*, model_name: str):
    def wrapper(cls):
        class Serializer(migrations.serializer.BaseSerializer):
            def serialize(self):
                return (
                    f"{cls.__module__}.{model_name}.{cls.__name__}.Schema()",
                    {f"import {cls.__module__}"},
                )

        setattr(
            cls.Schema,
            "__eq__",
            lambda s, o: s.dumps({}) == o.dumps({}),
        )
        migrations.writer.MigrationWriter.register_serializer(cls.Schema, Serializer)
        return cls

    return wrapper
