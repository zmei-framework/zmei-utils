

from json import JSONEncoder

from django.db.models import QuerySet, Model

from zmei.serializer import get_model_serializer


class ZmeiReactJsonEncoder(JSONEncoder):
    def __init__(self, *, view=None, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                         allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators,
                         default=default)
        if not view:
            raise AttributeError('ZmeiReactJsonEncoder: View is required')
        self.view = view

        self.serializers_cache = {}

    def get_model_serializer(self, model):
        if model not in self.serializers_cache:
            self.serializers_cache[model] = get_model_serializer(model)

        return self.serializers_cache[model]

    def default(self, o):
        # url object
        if hasattr(o, '__name__') and o.__name__ == 'url':
            return self.view.kwargs

        if isinstance(o, QuerySet):
            serializer = self.get_model_serializer(o.model)
            return serializer(o, many=True).data

        if isinstance(o, Model):
            serializer = self.get_model_serializer(o)
            return serializer(o).data

        print(f'WARN: ZmeiReactJsonEncoder -> Do not know how to encode "{o.__class__}"', o)
        return None
