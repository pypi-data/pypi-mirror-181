import configparser
import os

class Config(object):
    ConfMap = {}
    def __init__(self, config_file_path, env='DEV'):
        self.config = configparser.ConfigParser()
        self.config_file_path = config_file_path
        # prevent configparser convert all config keys to lower key
        self.config.optionxform = str
        self.config.read(config_file_path)
        self.env = env
        self.__ConfigMapper()

    def __ConfigMapper(self):
        for section in self.config.sections():
            section_dict = {}
            for key, val in self.config.items(section):
                section_dict[key] = val
                self.ConfMap[str(section)] = section_dict
        
        if self.env is None:
            self.ConfMap = self.ConfMap['DEV']

        if self.env.lower() == 'prod':
            self.ConfMap = self.ConfMap['PROD']
        else:
            self.ConfMap = self.ConfMap['DEV']

    def getValue(self, key):
        value = ''
        try:
            value = self.ConfMap[key]
        except KeyError as key:
            print('Key ' + key + ' did not found in config file')
        return value

    def __resp__(self):
        return f"<Config: {self.config_file_path}>"

    __str__ = __resp__