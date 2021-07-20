import os
from threading import Thread
from AsnDecoder import AsnDecoder


class CDR:
    def __init__(self, path):
        self.__path = path
        self.__filename = self.__path.replace('/', '\\').split('\\')[-1]
        self.__timestamp = int(self.__filename[7:17])
        self.onReady = False
        # Запускаем парсер в отдельном потоке
        Thread(target=self.__decode, daemon=True).start()

    def __decode(self):
        AsnDecoder.decode(file=self.__filename)
        self.onReady = True

    def readyToPush(self):
        return self.onReady

    def getTimestamp(self):
        return self.__timestamp

    def getPath(self):
        return self.__path

    def getFilename(self):
        return self.__filename

    def getDecodedFilePath(self):
        return self.getPath() + '.csv'

    def delete(self):
        try:
            os.remove(self.__path)
            if self.onReady:
                os.remove(self.getDecodedFilePath())
        except:
            pass
