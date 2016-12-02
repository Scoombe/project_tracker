"""test cases for the commit_controller"""
import sys
import os.path
#adding the files to the sys path that are in the diretory above, so that if the test is run directly
#you will be able to see the modules from the directory above.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Controllers import commit_controller
from Controllers import project_controller
import time
import sqlite3
import unittest
#getting the path of the databases in the diectory aboce and in the data folder
dbfile = os.path.realpath('../project_startup/Data/test.db')
def createchangesqlite3test():
    """Creating a change for testing, returns the expected and actual changes in a dictionary"""
    #calling the create project function defined in this file
    createProject()
    #getting the attributes from the create attributes
    # function this builds a dictionary with test attributes in
    attributes = createAttributes()
    #creating a new instance of a controller
    contoller = commit_controller.controler(dbname=dbfile)
    #calling the create change method from the commit controller class
    contoller.createChangeSQLITE3(attributes)
    change_id = getChangeID()
    #needs the calculated change_id is the commits are in a dictionary
    last_change = contoller.commits_dict[str(change_id)].toDict()
    #return the actual data and the expeceted data.
    return {"expected":{"change_id": change_id,"project_id":1, "description":"testing the createChangeTestMethod",
                        "date_of_change": attributes["date_of_change"],"file": "test.py", "author": "test test"},
            "actual": last_change}

def createProject():
    """functino fo creating a project, takes no parameters"""
    attributes = {"author":"samuel coombe", "description":"project for testing", "date_of_creation":time.strftime('%d/%m/%y'),
                  "language":"python","name":"test"}
    controller = project_controller.controller(dbname=dbfile)
    controller.createProjectSQLITE3(attributes)


def clearTestDB():
    """Removing anything added to the test database in the tests so that database tests are reproducable"""
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("DELETE FROM change;")
    c.execute("DELETE FROM project;")
    conn.commit()
    conn.close()

def createAttributes():
    """function for building attributes for a correct change"""
    date = time.strftime('%d/%m/%y')
    description = "testing the createChangeTestMethod"
    attributes = {"project_id": 1, "author": "test test", "file": "test.py", "date_of_change": date,
                  "description": description}
    return attributes

def getChangeID():
    """getting the last change from the commit controller"""
    change_id = 1
    # getting the change id from the test database
    conn = sqlite3.connect(dbfile)
    # the sql for getting the right data
    changes = conn.execute("SELECT CHANGE_ID FROM change")
    # looping round all of the returned rows from the database
    for change in changes.fetchall():
        if change[0] >= change_id:
            change_id = int(change[0])
    return  change_id


def checkLastChange():
    """Returning the last change from the test.db file"""
    commits = commit_controller.getChangesSQLITE3(dbfile)
    last_change = commits[len(commits) - 1]
    return last_change.toDict()

#unit test for the commitChange controller
class commitChangeTest(unittest.TestCase):
    def testCreate(self):
        """test for creating a change to the test database"""
        result = createchangesqlite3test()
        self.assertEqual(result["expected"],result["actual"])
    def testcreateWrongProjectIDTest(self):
        """Test that when you add  a change with the wrong project Id it isn't accepted"""
        attributes = createAttributes()
        attributes["project_id"] = 30
        controller = commit_controller.controler(dbfile)
        self.assertEquals(controller.createChangeSQLITE3(attributes),False)
    def testupdateChangeTest(self):
        """test for the updating of a change"""
        attributes = createAttributes()
        attributes["change_id"] = getChangeID()
        controller = commit_controller.controler(dbfile)
        controller.createChangeSQLITE3(attributes)
        attributes["description"] = "this is an updated description"
        attributes["author"] = "updated author"
        attributes["file"] = "updated file"
        controller.updateChangeSQLITE3(attributes)
        last_commit = controller.commits[0].toDict()
        self.assertEquals(last_commit["description"],"this is an updated description")
        self.assertEquals(last_commit["author"],"updated author")
        self.assertEquals(last_commit["file"],"updated file")

clearTestDB()
unittest.main()