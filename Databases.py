import psycopg2
from CdrFile import CDR


class PG:
    def __init__(self, host, user, password, dbname, table):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.table = table
        self.excepted = False

    def getConnection(self):
        conn = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname)
        cursor = conn.cursor()
        cursor.execute('SET DateStyle=\'YMD\';')
        return conn, cursor

    def createTable(self, argsCount):
        conn, cursor = self.getConnection()
        request = f"CREATE TABLE IF NOT EXISTS %s ( %s )"
        args = []
        for arg in range(argsCount):
            args.append('arg' + str(arg) + ' text')
        argString = ','.join(args)
        cursor.execute(request % (self.table, argString))
        conn.commit()


    def copyFromFile(self, file):
        result = False
        print(type(file), file)
        try:
            conn, cursor = self.getConnection()
            openedFile = open(file.getDecodedFilePath(), 'r')
            cursor.copy_from(openedFile, self.table, sep=';')
            conn.commit()
            result = True
        except:
            if not self.excepted:
                with open(file.getDecodedFilePath(), 'r') as decodedFile:
                    line = decodedFile.readline()
                    self.createTable(len(line.split(';')))
                    return self.copyFromFile(file)

        openedFile.close()
        file.delete()
        return result
