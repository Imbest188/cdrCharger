import configparser


class SettingManager:
    def __init__(self):
        self.config = self.__readConfig()

    def __defaultConfig(self):
        config = configparser.ConfigParser()
        config['FTP'] = {'host': '10.5.5.254', 'user': 'stat', 'password': 'mp26NokdpPpkM'}
        config['FtpPath'] = {'MSS1': '/msc/MSSLUG01/CHARGING/', 'MSS2': '/msc/MSSLUG02/CHARGING/'}
        config['Database'] = {'host': '10.5.5.254', 'user': 'smena', 'password': 'postgres20094',
                              'dbname': 'mss', 'table': 'cdr'}
        config['Bot'] = {'token': ''}
        config['WhiteList'] = {'chat': 'id'}

        with open('settings.ini', 'w+') as configfile:
            config.write(configfile)
        return config

    def __readConfig(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        if not len(config.sections()):
            return SettingManager().defaultConfig()
        return config

    def makeDict(self, keys, values):
        result = dict()
        for iter in range(len(keys)):
            result.update({keys[iter]: values[iter]})
        return result

    def getValues(self, arg):
        keys = list(self.config[arg].keys())
        values = list(self.config[arg].values())
        return self.makeDict(keys, values)

    def getDatabaseSettings(self):
        dbset = self.getValues('Database')
        host = dbset['host']
        login = dbset['user']
        password = dbset['password']
        dbname = dbset['dbname']
        table = dbset['table']
        return host, login, password, dbname, table

    def getFtpSettings(self):
        ftpset = self.getValues('FTP')
        host = ftpset['host']
        login = ftpset['user']
        password = ftpset['password']
        folders = self.getValues('FtpPath')
        return host, login, password, folders

    def getBotSettings(self):
        return self.getValues('Bot')
