from configparser import ConfigParser, DuplicateSectionError


class ConfigHelper:

    def __init__(self, configFile):
        self.config = ConfigParser()
        self.conFile = configFile

    # creates a config if non exists
    def createConfig(self, section):
        try:
            self.config.read(self.conFile)
            self.config.add_section(section)

            self.config.write(open(self.conFile, 'w'))
        except DuplicateSectionError:
            pass

    def addConfigLine(self, section, key, value):
        # sets config to read from and sets the parameters
        self.config.read(self.conFile)
        self.config.set(section, key, value)

        # writes changes out to config
        with open('backup_config.ini', 'w') as outLine:
            self.config.write(outLine)

    def getLineValue(self, section, key):
        return self.config.get(section, key)
