import sqlite3
class controller():
    def __init__(self,dbname):
        self.dbname = dbname
    def DatabaseTransaction(self, sqlite_query, parameters):
        """Function for the querying of a database"""
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()

        print (sqlite_query)
        curs.execute(sqlite_query,parameters)
        conn.commit()
        conn.close()
