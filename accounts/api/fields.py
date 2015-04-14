from django.core.exceptions import ValidationError
from bitfield import BitHandler
from rest_framework import serializers

from ..models import Developer


class SerializedBitField(serializers.Field):
    def to_internal_value(self, data):
        result = BitHandler(0, [k for k, v in Developer.PROJECT_PREFERENCES_FLAGS])
        for k in data:
            try:
                setattr(result, str(k), True)
            except AttributeError:
                raise ValidationError('Unknown choice: %r' % (k,))
        return int(result)

    def to_representation(self, value):
        result = []
        for v in value:
            if v[1]:
                result.append(v[0])
        return result


class SerializedBareField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value
