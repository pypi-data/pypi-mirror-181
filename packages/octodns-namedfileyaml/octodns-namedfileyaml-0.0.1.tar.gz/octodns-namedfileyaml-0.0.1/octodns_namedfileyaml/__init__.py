#
#
#
from os.path import join

from octodns.provider.yaml import YamlProvider

__VERSION__ = '0.0.1'


class NamedFileYamlProvider(YamlProvider):
    def __init__(self, id, filename, *args, **kwargs):
        super().__init__(id, *args, **kwargs)
        self.filename = filename

    def get_filenames(self, zone):
        return join(self.directory, f'{self.filename}.yaml')
