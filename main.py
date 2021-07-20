import os
import time
from Worker import Worker
from Settings import SettingManager as settings


def makeCdrFolder():
    try:
        os.mkdir('CDR')
    except:
        pass

def initWorker():
    worker = Worker()
    ftpHost, ftpLogin, ftpPassword, ftpFolders = initSettings.getFtpSettings()
    worker.setupFtp(ftpHost, ftpLogin, ftpPassword, ftpFolders)
    host, login, password, dbname, table = initSettings.getDatabaseSettings()
    worker.setupDatabase(host, login, password, dbname, table)
    return worker

if __name__ == '__main__':
    initSettings = settings()
    makeCdrFolder()

    worker = initWorker()
    while True:
        if not worker.checkNewFiles():
            time.sleep(60)
