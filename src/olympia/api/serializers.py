from collections import defaultdict
from datetime import datetime

from django.conf import settings

from elasticsearch_dsl.response.hit import Hit
from rest_framework import serializers

from olympia.zadmin.models import get_config

from .fields import (
    ESTranslationSerializerField,
    OutgoingESTranslationField,
    OutgoingTranslationField,
    TranslationSerializerField,
)


class BaseESSerializer(serializers.ModelSerializer):
    """
    A base deserializer that handles ElasticSearch data for a specific model.

    When deserializing, an unbound instance of the model (as defined by
    fake_object) is populated with the ES data in order to work well with
    the parent model serializer (e.g., AddonSerializer).

    """

    # In base classes add the field names we want converted to Python
    # datetime from the Elasticsearch datetime strings.
    datetime_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set all fields as read_only just in case.
        for field_name in self.fields:
            self.fields[field_name].read_only = True

    def get_fields(self):
        """
        Return all fields as normal, with one exception: replace every instance
        of TranslationSerializerField with ESTranslationSerializerField.
        """
        fields = super().get_fields()
        for key, field in fields.items():
            if isinstance(field, OutgoingTranslationField):
                fields[key] = OutgoingESTranslationField(source=field.source)
            elif isinstance(field, TranslationSerializerField):
                fields[key] = ESTranslationSerializerField(source=field.source)
        return fields

    def to_representation(self, data):
        es_meta = defaultdict(lambda: None)
        # Support `Hit` instances to allow passing in ElasticSearch
        # results directly into the serializer.
        if isinstance(data, Hit):
            es_meta = data.meta
            data = data.to_dict()

        obj = self.fake_object(data)
        obj._es_meta = es_meta
        result = super().to_representation(obj)
        return result

    def fake_object(self, data):
        """
        Create a fake model instance from ES data which serializer fields will
        source from.
        """
        raise NotImplementedError

    def handle_date(self, value):
        if not value:
            return None

        # Don't be picky about microseconds here. We get them some time
        # so we have to support them. So let's strip microseconds and handle
        # the datetime in a unified way.
        value = value.partition('.')[0]
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

    def _attach_fields(self, obj, data, field_names):
        """Attach fields to fake instance."""
        for field_name in field_names:
            value = data.get(field_name, None)
            if field_name in self.datetime_fields and value:
                value = self.handle_date(value)
            setattr(obj, field_name, value)
        return obj

    def _attach_translations(self, obj, data, field_names):
        """Deserialize ES translation fields."""
        for field_name in field_names:
            if field_name in self.fields:
                self.fields[field_name].attach_translations(obj, data, field_name)
        return obj


class SiteStatusSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'read_only': settings.READ_ONLY,
            'notice': get_config('site_notice'),
        }
