import re

from glob import glob
from os import path
# from pprint import pprint
from importlib import import_module


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
        with open(self.filename, 'r') as file:
            for match in self.RE_CLASS.findall(file.read()):
                child = match[0]
                parents = [
                    parent.strip()
                    for parent in match[1].split(',') if parent.strip()
                ]
                self.classes[child] = {
                    'parents': parents,
                    'fullparents': [],
                    'name': child,
                }

        module_dotted = self.find_module()
        if module_dotted:
            module = import_module(module_dotted)
            for name, data in self.classes.items():
                cls = getattr(module, name)
                fullname = cls.__module__ + '.' + cls.__name__
                data['fullname'] = fullname

                for parent_name in data['parents']:
                    if parent_name in ['object', 'Exception', 'dict']:
                        # data['fullparents'].append(parent_name)
                        pass
                    else:
                        parent = getattr(module, parent_name)
                        data['fullparents'].append(
                            parent.__module__ + '.' + parent.__name__
                        )
        else:
            print('No module:', self.filename)
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

    def __init__(self):
        self.all_classes = {}

    def run(self):
        self.search_for_classes()
        self.generate_graph()

    def search_for_classes(self):
        for filename in FindAllClasses('..').run():
            self.all_classes.update(
                Converter(filename).run()
            )

    def generate_graph(self):
        with open('graph.dot', 'w') as file:
            file.write('digraph {\n')

            names = []

            for child, data in self.all_classes.items():
                names.append(
                    ' "%s" [label="%s"];' % (
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

GraphCreator().run()
# conv = Converter(
#     '/home/socek/projects/impaf/example/src/impex/application/controller.py')
# pprint(conv.run())
