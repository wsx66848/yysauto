from configparser import ConfigParser

class Config(ConfigParser):

    def getTuple(self, section, option, sep=',', value=int):
        value_str = super().get(section, option)
        return tuple([value(x) for x in value_str.split(sep)]) 