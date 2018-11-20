from django.views.generic.base import View, ContextMixin, TemplateResponseMixin


class ImproperlyConfigured(Exception):
    pass


class _Data(object):
    def __init__(self, data=None):
        self.__dict__.update(data or {})

    def __add__(self, data):
        return _Data({**self.__dict__, **data})


class ZmeiDataViewMixin(ContextMixin, View):
    _data = None

    def get_data(self, url, request, inherited):
        return {}

    def _get_data(self):
        if not self._data:
            self._data = self.get_data(
                url=type('url', (object,), self.kwargs),
                request=self.request,
                inherited=False
            )

        return self._data

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        return {**context_data, **self._get_data()}


class CrudView(TemplateResponseMixin):
    def render_to_response(self, context, **response_kwargs):
        return context


class CrudMultiplexerView(TemplateResponseMixin, ContextMixin, View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.crud_views = {}
        for cls in self.get_crud_views():
            crud = cls(*args, **kwargs)
            self.crud_views[crud.name] = crud

    def get_crud_views(self):
        return ()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['crud'] = {}
        for crud in self.crud_views.values():
            self.populate_crud(args, crud, kwargs, request)

            context['crud'][crud.name] = crud.get(request, *args, **kwargs)

        return self.render_to_response(context)

    def populate_crud(self, args, crud, kwargs, request):
        crud.request = request
        crud.args = args
        crud.kwargs = kwargs

    def post(self, request, *args, **kwargs):
        form_name = request.POST.get('_form')
        crud = self.crud_views.get(form_name)

        self.populate_crud(args, crud, kwargs, request)

        if not crud:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return crud.post(request, *args, **kwargs)
