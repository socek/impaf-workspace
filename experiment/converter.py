import re

from glob import glob
from os import path
# from pprint import pprint
from importlib import import_module
from inspect import getmro


class DataExcept(Exception):

    def __init__(self):
        self.modules = []

    def append(self, name):
        self.modules.append(name)

    def get_dotted_module(self):
        return '.'.join(self.modules)


class Converter(object):
    RE_CLASS = re.compile(
        '^\s*class ([-_a-zA-Z0-9]*)\((.*?)\):$',
        re.MULTILINE | re.DOTALL,
    )

    def __init__(self, filename):
        self.filename = filename
        self.classes = {}

    def find_module(self):
        name = path.basename(self.filename)[:-3]
        try:
            self._find_module(self.filename)
        except DataExcept as er:
            if name == '__init__':
                return er.get_dotted_module()
            else:
                return er.get_dotted_module() + '.' + name

    def _find_module(self, filename):
        filename = filename or self.filename
        dirname = path.dirname(filename)
        init_filename = path.join(dirname, '__init__.py')

        if path.exists(init_filename):
            try:
                if not self._find_module(dirname):
                    raise DataExcept()
            except DataExcept as er:
                er.append(path.basename(dirname))
                raise er
        else:
            return False

    def run(self):
        module_dotted = self.find_module()
        if module_dotted:
            module = import_module(module_dotted)

        with open(self.filename, 'r') as file:
            for match in self.RE_CLASS.findall(file.read()):
                child = match[0]
                parents = [
                    parent.strip()
                    for parent in match[1].split(',') if parent.strip()
                ]
                data = {
                    'parents': parents,
                    'fullparents': [],
                    'name': child,
                }
                fullname = None
                if module_dotted:
                    cls = getattr(module, child)
                    fullname = cls.__module__ + '.' + cls.__name__
                    data['fullname'] = fullname
                    data['mro'] = [
                        mcls.__module__ + '.' + mcls.__name__
                        for mcls in getmro(cls)
                        if not mcls.__module__.startswith('builtins')
                    ]

                    for parent_name in data['parents']:
                        if parent_name in ['object', 'Exception', 'dict']:
                            # data['fullparents'].append(parent_name)
                            pass
                        else:
                            parent = getattr(module, parent_name)
                            data['fullparents'].append(
                                parent.__module__ + '.' + parent.__name__
                            )
                name = fullname or child
                self.classes[name] = data
        return self.classes


class FindAllClasses(object):

    def __init__(self, startpoint):
        self.startpoint = startpoint

    def run(self):
        pathname = path.join(self.startpoint, '*')
        for filename in glob(pathname):
            if self._is_dir_enabled(filename):
                yield from self.search_for_class(filename)

    def _is_dir_enabled(self, filename):
        basename = path.basename(filename)
        return (
            path.isdir(filename)
            and not basename.startswith('venv')
            and not basename == 'experiment'
        )

    def search_for_class(self, dirname):
        pathname = path.join(dirname, '*')
        for filename in glob(pathname):
            if path.isdir(filename):
                yield from self.search_for_class(filename)
            elif filename.endswith('.py'):
                yield filename


class GraphCreator(object):

    def __init__(self, target_class=None):
        self.all_classes = {}
        self.target_class = target_class
        self._cache = []

    def run(self):
        self.search_for_classes()
        if self.target_class:
            self.mro = self.all_classes[self.target_class]['mro']
            # self.mro.insert(0, self.target_class)
        self.generate_graph()

    def search_for_classes(self):
        for filename in FindAllClasses('..').run():
            self.all_classes.update(
                Converter(filename).run()
            )

    def get_classes(self):
        if self.target_class:
            yield from self._get_classes_with_parents(self.target_class)
        else:
            yield from self.all_classes.values()

    def _get_classes_with_parents(self, target):
        data = self.all_classes[target]
        if id(data) not in self._cache:
            self._cache.append(id(data))
            yield data
            for parent in data['fullparents']:
                yield from self._get_classes_with_parents(parent)

    def generate_graph(self):
        with open('graph.dot', 'w') as file:
            file.write('digraph {\n')

            names = []

            for data in self.get_classes():
                if self.target_class:
                    names.append(
                        '  "%s" [label="%s (%d)"];' % (
                            data['fullname'],
                            data['name'],
                            self.mro.index(data['fullname']),
                        )
                    )
                else:
                    names.append(
                        '  "%s" [label="%s"];' % (
                            data['fullname'],
                            data['name'],
                        )
                    )
                for parent in data['fullparents']:
                    file.write(
                        '  "%s" -> "%s";\n' % (
                            parent,
                            data['fullname'],
                        )
                    )

            for name in names:
                file.write(name + '\n')

            file.write('}\n')

# GraphCreator('impex.orders.controllers.OrdersListController').run()
GraphCreator('impex.orders.controllers.OrdersListControllerEx').run()

# GraphCreator('implugin.test_beaker.ExampleBeakerApplication').run()
# GraphCreator().run()

# conv = Converter(
#     '/home/socek/projects/impaf/example/src/impex/application/controller.py')
# pprint(conv.run())
