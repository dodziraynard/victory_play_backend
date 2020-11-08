from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json
from django.template import Library
from django.forms.models import model_to_dict

from django.core import serializers
from django.db import models
from django.http import JsonResponse

JSONSerializer = serializers.get_serializer("json")


class JSONWithURLSerializer(JSONSerializer):

    def handle_field(self, obj, field):
        value = field.value_from_object(obj)
        if isinstance(field, models.FileField):
            self._current[field.name] = value.url
        else:
            return super(JSONWithURLSerializer, self).handle_field(obj, field)


register = Library()


def jsonify(object):
    obj = [object]
    # if isinstance(obj, QuerySet):
    serializer = JSONWithURLSerializer()
    return serializer.serialize(obj)
    # return json.dumps(obj)


register.filter('jsonify', jsonify)
