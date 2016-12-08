import sqlite3
class controller():
    def __init__(self,dbname):
        self.dbname = dbname
    def DatabaseTransaction(self, sqlite_query, parameters):
        """Function for the querying of a database"""
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()
        curs.execute(sqlite_query,parameters)
        conn.commit()
        conn.close()
    def DatabaseGet(self, sqlite_query,parameters = []):
        """function for returning the results as a list"""
        conn = sqlite3.connect(self.dbname)
        results = conn.execute(sqlite_query, parameters)
        results = results.fetchall()
        conn.close()
        return results
