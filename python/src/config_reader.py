import json
import os


class ConfigReader(object):

    __config_path = f'config/appsettings.json'

    database = None

    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)).replace('resources', ''), self.__config_path)
        with open(path, 'r') as config_file:
            config = json.loads(config_file.read())

            self.database = self.__get_section(config, 'database')

    @staticmethod
    def __get_section(config, section_name):
        if config[section_name] is not None:
            return config[section_name]
        else:
            raise MissingConfigSection(section_name)


class MissingConfigSection(Exception):
    __error_description = 'Missing configuration section -> "%s" please verify appsettings.config!'

    def __init__(self, section_name):
        super().__init__(self.__error_description % section_name)
