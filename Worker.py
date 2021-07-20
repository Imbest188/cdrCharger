from Ftp import Ftp
from Databases import PG
from datetime import datetime as dt
from datetime import timedelta as delta
import time
from threading import Thread


class FtpFolder:
    def __init__(self, ftpPath, name, days):
        self.days = days
        self.name = name
        self.path = ftpPath
        self.checkInitFile()
        self.lastFile = self.readLastFile()

    def getDefaultDate(self):
        defDate = dt.now() - delta(days=self.days)
        year = defDate.year - 2000
        result = defDate.strftime("%m%d%H%M")
        return int(str(year) + result)

    def getPath(self):
        return self.path

    def checkInitFile(self):
        try:
            with open(self.name, 'r+') as last:
                pass
        except:
            with open(self.name, 'w+') as last:
                pass

    def readLastFile(self):
        with open(self.name, 'r+') as last:
            point = last.read()
            if len(point) > 6:
                return int(point)
            else:
                return self.getDefaultDate()

    def extractFilename(self, filePath):
        return filePath.replace('\\', '/').split('/')[-1]

    def getTimestampInfo(self, filename):
        filename = self.extractFilename(filename)
        try:
            return int(filename[7:17])
        except:
            return 0

    def extractNewFiles(self, filesArray):
        result = []
        for file in filesArray:
            timestamp = self.getTimestampInfo(file)
            if timestamp > 0 and timestamp > self.lastFile:
                result.append(file)
        return result

    def updateLastTimestamp(self, timestamp):
        if timestamp > self.lastFile:
            self.lastFile = timestamp
            with open(self.name, 'w') as lastFile:
                lastFile.write(str(timestamp))



class Worker:
    def __init__(self):
        self.days = 1
        self.ftp = None
        self.db = None
        self.pathList = []
        self.filePool = []
        self.pooling = False

    def setupFtp(self, host, login, password, folders):
        self.ftp = Ftp(host, login, password)
        for folder in folders.keys():
            self.addPath(folders[folder], folder)

    def setupDatabase(self, host, login, password, dbname, table):
        self.db = PG(host, login, password, dbname, table)

    def addPath(self, path, name):
        path = FtpFolder(path, name, self.days)
        self.pathList.append(path)

    def __pushToDb(self):
        self.pooling = True
        while len(self.filePool):
            for file in self.filePool:
                if file.onReady:
                    self.db.copyFromFile(file)
                    file.delete()
                    self.filePool.remove(file)
            time.sleep(1)
        self.pooling = False

    def pushToDb(self):
        if not self.pooling:
            Thread(target=self.__pushToDb(), daemon=True).start()

    def checkNewFiles(self):
        isEmpty = True
        for path in self.pathList:
            files = self.ftp.list(path.getPath())
            newFiles = path.extractNewFiles(files)
            if len(newFiles) > 0:
                isEmpty = False
            for file in newFiles:
                while len(self.filePool) > 4:
                    time.sleep(1)
                cdrFile = self.ftp.download(file)

                self.filePool.append(cdrFile)
                self.pushToDb()
                path.updateLastTimestamp(cdrFile.getTimestamp())
        return isEmpty
