from ftpretty import ftpretty as ftplib
from CdrFile import CDR


class Ftp:
    def __init__(self, host, login, password):
        self.ftp = ftplib(host, login, password)
        self.host = host
        self.login = login
        self.password = password
        self.currentPath = []

    def list(self, path=''):
        if not len(path):
            path = self.getCurrentPath()
        try:
            return self.ftp.list(path)
        except:
            self.ftp = ftplib(self.host, self.login, self.password)
            return self.ftp.list(path)

    def getCurrentPath(self):
        path = '/'
        if len(self.currentPath):
            path += '/'.join(self.currentPath)
            path += '/'
        return path

    def getFilename(self, path):
        return path.replace('\\', '/').split('/')[-1]

    def download(self, remotePath, localPath='CDR/'):
        filename = self.getFilename(remotePath)
        with open(localPath + filename, 'wb+') as downloadingFile:
            try:
                self.ftp.get(remotePath, downloadingFile)
            except:
                self.ftp = ftplib(self.host, self.login, self.password)
                self.ftp.get(remotePath, downloadingFile)
        return CDR(localPath + filename)
