"""test cases for the commit_controller"""
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print(os.path.join(os.path.dirname(__file__), '..'))
from Controllers import commit_controller
from Controllers import project_controller
import time
import sqlite3
import unittest

dbfile = os.path.realpath('../project_startup/Data/test.db')
"""test for the creation of a valid change"""
def createchangesqlite3test():
    createProject()
    attributes = createAttributes()
    contoller = commit_controller.controler(dbname=dbfile)
    contoller.createChangeSQLITE3(attributes)
    last_change = contoller.commits[len(contoller.commits) - 1].toDict()
    return {"expected":{"change_id": 1,"project_id":1, "description":"testing the createChangeTestMethod",
                        "date_of_change": attributes["date_of_change"],"file": "test.py", "author": "test test"},
            "actual": last_change}

def createProject():
    attributes = {"author":"samuel coombe", "description":"project for testing", "date_of_creation":time.strftime('%d/%m/%y'),
                  "language":"python","name":"test"}
    controller = project_controller.controller(dbname=dbfile)
    controller.createProjectSQLITE3(attributes)

"""Removing anything added to the test database"""
def clearTestDB():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("DELETE FROM change;")
    c.execute("DELETE FROM project;")
    conn.commit()
    conn.close()
"""
function for building attributes for a correct change
"""
def createAttributes():
    date = time.strftime('%d/%m/%y')
    description = "testing the createChangeTestMethod"
    attributes = {"project_id": 1, "author": "test test", "file": "test.py", "date_of_change": date,
                  "description": description}

    return attributes

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
        attributes = createAttributes()
        controller = commit_controller.controler
        self.assertEquals(controller.createChangeSQLITE3(attributes),False)


clearTestDB()
unittest.main()