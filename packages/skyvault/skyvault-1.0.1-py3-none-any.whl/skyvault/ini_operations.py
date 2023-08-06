import abc
import configparser

from .aes import AESCipher
from PenguinServices import pathExists, openFile

class ConfigurationUtils(abc.ABC):
    @classmethod
    def display_rows(cls, rows):
        for row in rows:
            print(row)        
            
    @staticmethod
    def write(configuration_file, configuration_parser):
        with open(configuration_file, 'w') as configfile:
            configuration_parser.write(configfile) 

    def __init__(self, password, configuration_file: str):
        if pathExists(configuration_file) is False:
            try:
                openFile(configuration_file, option="w")
            except Exception as e:
                raise Exception(e)
        
        self.crypto = AESCipher(password)
        self.config = configparser.ConfigParser()
        self.configuration_file = configuration_file
        
    def read(self):
        self.config.read(self.configuration_file)
        
    # "section" : [{"key": "KEY", "value": "VALUE"}]
    def add_information(self, new_information: dict):
        for section, values in new_information.items():
            if section not in self.get_sections():
                self.config[section] = {}
                
            for item in values:
                self.config[section][item['key']] = self.crypto.encrypt(item['value'])
                # item['value']
                
        self.write(self.configuration_file, self.config)
        
    def new_file_write(self, filename):
        self.write(filename, self.config)

    def get_sections(self):
        return self.config.sections()
        
    def to_json(self):
        result = {}
        
        for section in self.get_sections():
            result[section] = {}
            for key in self.config[section]:
                result[section][key] = self.crypto.decrypt(self.config[section][key])
                # self.config[section][key]
                
        return result
        
    @abc.abstractmethod
    def parse_printer(self, *args, **kwargs):
        pass
        
class LinuxConfigParser(ConfigurationUtils):
    def __init__(self, password, configuration_file = 'test.ini', configuration_folder = '/usr/Sphinx/config/'):
        self.destination = f'{configuration_folder}{configuration_file}'
        super().__init__(password, self.destination)
        
    def parse_printer(self, *args, **kwargs):
        print(self.get_sections())
        for section in self.get_sections():
            print(f'Section: {section}')
            for key in self.config[section]:
                print(f'Key: {key}, Value: {self.crypto.decrypt(self.config[section][key])}')
                # {self.config[section][key]}')
                
            print()
            
if __name__ == "__main__":
    user_config = LinuxConfigParser('Darlins@12345678')
    user_config.read()

    information = {"postgresql": [{"key": "host", "value": "localhost"}, {"key": "port", "value": "1337"}], "DEFAULT": [{"key": "ip", "value": "127.0.0.1"}]}
    
    user_config.add_information(information)
      
    user_config.parse_printer() 
    print(user_config.to_json())
    user_config.new_file_write('/tmp/file.ini')
