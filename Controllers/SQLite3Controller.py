import sqlite3
class controller():
    def __init__(self,dbname):
        self.dbname = dbname
    def DatabaseTransaction(self, sqlite_query, *args):
        """Function for the querying of a database"""
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()
        wildString =  ""
        arguments = []
        count = 0
        for arg in args:
            #a string for the constucrion of the wild card string
            arguments.append(arg)
            count = count + 1
        if count == 0:
            curs.execute(sqlite_query)
        else:
            curs.execute(sqlite_query,arguments)
        conn.commit()
        conn.close()
