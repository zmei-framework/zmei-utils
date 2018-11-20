from django.db.models import QuerySet, Model
from django.utils.module_loading import import_string
from rest_framework import serializers


class DefaultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        exclude = []


def create_default_serializer(model):
    serializer = type('_', (DefaultModelSerializer,), {})
    serializer.Meta.model = model

    return serializer


def get_model_serializer(model, descriptor='_', strict=False):
    serializer = None
    try:
        index_import_path = f"{'.'.join(model.__module__.split('.')[:-1])}.serializers.index"
        serializer_index = import_string(index_import_path)

        if model in serializer_index:
            serializer = serializer_index[model].get(descriptor)
            if not serializer and strict:
                raise AttributeError(f'Serializer with name "{descriptor}" does not exist for model "{model}"')
    except ImportError:
        pass

    if not serializer:
        serializer = create_default_serializer(model)

    return serializer


def serialize(qs_or_model, descriptor='_'):
    if isinstance(qs_or_model, QuerySet):
        model = qs_or_model.model
        many = True
    elif isinstance(qs_or_model, Model):
        model = qs_or_model
        many = False
    else:
        raise AttributeError('serialize method accept only QuerySet or Model. Given: ', type(qs_or_model))

    return get_model_serializer(model, descriptor=descriptor, strict=True)(qs_or_model, many=many).data