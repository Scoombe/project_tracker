"""test cases for the commit_controller"""
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print(os.path.join(os.path.dirname(__file__), '..'))
from Controllers import commit_controller
import time
import sqlite3
import unittest

dbfile = os.path.realpath('../project_startup/Data/test.db')
"""test for the creation of a valid change"""
def createchangesqlite3test():
    print("dbfile: " + dbfile)
    date = time.strftime('%d/%m/%y')
    description = "testing the createChangeTestMethod"
    attributes = {"project_id": 1, "author": "test test", "file": "test.py", "date_of_change": date,
                  "description": description}
    commit_controller.createChangeSQLITE3(attributes,dbname=dbfile)
    last_change = checkLastChange()
    print(last_change)
    return {"expected":{"change_id": 1,"project_id":1, "description":description, "date_of_change": date,
            "file": "test.py", "author": "test test"},
            "actual": last_change}

"""Removing anything added to the test database"""
def clearTestDB():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("DELETE FROM change;")
    conn.commit()
    conn.close()

"""Returning the last change from the test.db file"""
def checkLastChange():
    commits = commit_controller.getChangesSQLITE3(dbfile)
    last_change = commits[len(commits) - 1]
    return last_change.toDict()
#unit test for the commitChange controller
class commitChangeTest(unittest.TestCase):
    def testCreate(self):
        """test for creating a change to the test database"""
        result = createchangesqlite3test()
        self.assertEqual(result["expected"],result["actual"])
    def createWrongProjectID(self):
        """Test that when you add  a change with the wrong project Id it isn't accepted"""

clearTestDB()
unittest.main()