import os
from io import TextIOWrapper

from py_mini_racer.py_mini_racer import MiniRacerBaseException
from py_mini_racer import py_mini_racer

from .views import ZmeiDataViewMixin
from zmei.json import ZmeiReactJsonEncoder
from zmei.react import ZmeiReactServer

class ZmeiReactServer(object):
    def __init__(self):
        super().__init__()

        self.loaded_files = []
        self.loaded_files_mtime = {}

        self.jsi = None

        self.checksum = None

    def reload_interpreter(self):
        self.jsi = py_mini_racer.MiniRacer()

        code = """
        var global = this;
        var module = {exports: {}};
        var setTimeout = function(){};
        var clearTimeout = function(){};var console = {
            error: function() {},
            log: function() {},
            warn: function() {}
        };
        """

        self.jsi.eval(code)

        for filename in self.loaded_files:
            self.loaded_files_mtime[filename] = os.path.getmtime(filename)
            self.eval_file(filename)

    def autreload(self):
        if len(self.loaded_files_mtime) == 0:
            return

        for filename in self.loaded_files:
            if self.loaded_files_mtime[filename] != os.path.getmtime(filename):
                print('Reloading ZmeiReactServer')
                self.reload_interpreter()
                break

    def evaljs(self, code):
        if not self.jsi:
            self.reload_interpreter()

        return self.jsi.eval(code)

        # except JSRuntimeError as e:
        #     message = str(e)
        #
        #     message = '\n' + colored('Error:', 'white', 'on_red') + ' ' + message
        #
        #     print(message)
        #     m = re.search('\(line\s+([0-9]+)\)', message)
        #     if m:
        #         print('-' * 100)
        #         print('Source code:')
        #         print('-' * 100)
        #         row = int(m.group(1)) - 1
        #         source = code.splitlines()
        #
        #         line = colored(source[row], 'white', 'on_red')
        #         print('\n'.join([f'{x+1}:\t{source[x]}' for x in range(max(0, row - 10), row)]))
        #         print(f'{row+1}:\t{line}')
        #         print('\n'.join([f'{x+1}:\t{source[x]}' for x in range(row + 1, min(row + 10, len(source) - 1))]))
        #         print('-' * 100)

    def load(self, filename):
        self.loaded_files.append(filename)

    def eval_file(self, filename):
        with open(filename) as f:
            self.evaljs(f.read())



class ZmeiReactViewMixin(ZmeiDataViewMixin):

    react_server = None
    react_components = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if 'application/json' in self.request.META['HTTP_ACCEPT']:
            return HttpResponse(context['react_state'], content_type='application/json')

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if not isinstance(self.react_server, ZmeiReactServer):
            raise ImproperlyConfigured('ZmeiReactViewMixin requires react_server property')

        if not isinstance(self.react_components, list):
            raise ImproperlyConfigured('ZmeiReactViewMixin requires react_component property')

        data['react_state'] = ZmeiReactJsonEncoder(view=self).encode(self._get_data())

        if settings.DEBUG:
            self.react_server.autreload()

        for cmp in self.react_components:
            try:
                data[f'react_page_{cmp}'] = self.react_server.evaljs(f"R.renderServer(R.{cmp}Reducer, R.{cmp}, {data['react_state']});")
            except MiniRacerBaseException as e:
                data[f'react_page_{cmp}'] = f'<script>var err = {json.dumps({"msg": str(e)})}; ' \
                                            f'document.body.innerHTML = ' \
                                            "'<h2>Error rendering React component. See console for details.</h2>' + " \
                                            f'"<pre>" + err.msg + "</pre>" + document.body.innerHTML;</script>'

        return data
