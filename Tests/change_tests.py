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
import logging
logger = logging.getLogger("change_tests")
logger.setLevel(logging.INFO)

#getting the path of the databases in the diectory aboce and in the data folder
dbfile = os.path.realpath('../project_startup/Data/test.db')
def createchangesqlite3test():
    """Creating a change for testing, returns the expected and actual changes in a dictionary"""
    logger.debug("change_test: createchangesqlite3Test: Creating a new change")
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
    return {"expected":{"change_id": change_id,"project_id":getProjectID(), "description":"testing the createChangeTestMethod",
                        "date_of_change": attributes["date_of_change"],"file": "test.py", "author": "test test"},
            "actual": last_change}

def createProject():
    """functino fo creating a project, takes no parameters"""
    attributes = {"author":"samuel coombe", "description":"project for testing", "date_of_creation":time.strftime('%d/%m/%y'),
                  "language":"python","name":"test"}
    controller = project_controller.controller(dbname=dbfile)
    controller.createProjectSQLITE3(attributes)
    logger.debug("change_tests: createProject: creating a project for the project to use:  {}".format(str(controller.projects[-1].toDict())))


def clearTestDB():
    logger.debug("change_tests: clearTestDB: clearing up the test by deleting from the change and project files")
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
    #calling get project ID from the get project ID
    attributes = {"project_id": getProjectID(), "author": "test test", "file": "test.py", "date_of_change": date,
                  "description": description}
    logger.debug("cahgne_tests: createAttributes: creating change attribues {}".format(str(attributes)))
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
    logger.debug("change_test:getChangeID: creating a change_id for a change: {}".format(str(change_id)))
    return change_id

def getProjectID():
    controller = project_controller.controller(dbfile)
    project = controller.projects
    project_id = project[-1].toDict()["project_id"]
    logger.debug("change_tests:getProjectID: creating a project_id for a change to use: {}".format(str(project_id)))
    return project_id

def checkLastChange():
    """Returning the last change from the test.db file"""
    controller = commit_controller.controler(dbfile)
    commits = controller.commits
    last_change = commits[len(commits) - 1]
    logger.debug("change_tests: checkLastChange: returning the last change: {}".format(str(last_change.toDict())))
    return last_change.toDict()

def getProjectId():
    """function for getting the last project_id"""
    project_id = 1
    # getting the change id from the test database
    conn = sqlite3.connect(dbfile)
    # the sql for getting the right data
    projects = conn.execute("SELECT PROJECT_ID FROM project")
    # looping round all of the returned rows from the database
    for project in projects.fetchall():
        if project[0] >= project_id:
            project_id = project[0]
        logger.debug("change_tests: getProjectID: getting a project_id for a change to use using sql: {}".format(str(project_id)))
    return project_id


#unit test for the commitChange controller
class commitChangeTest(unittest.TestCase):
    def testCreate(self):
        """test for creating a change to the test database"""
        result = createchangesqlite3test()
        self.assertEqual(result["expected"],result["actual"])
    def testCreateWrongProjectID(self):
        """Test that when you add  a change with the wrong project Id it isn't accepted"""
        logger.debug("=============WrongProjectID=================")
        attributes = createAttributes()
        attributes["project_id"] = 30
        logger.debug("change_tests: testCreateWrongProjectId: creating a project with the wrong project_id: {}"
                      .format(str(attributes)))
        controller = commit_controller.controler(dbfile)
        #expecting an error string from this call
        valid = controller.createChangeSQLITE3(attributes)
        self.assertEqual(valid,"valid Attributes error: True project id errors: invalid project key")

    def testupdateChangeTest(self):
        """test for the updating of a change"""
        attributes = createAttributes()
        attributes["change_id"] = getChangeID()
        controller = commit_controller.controler(dbfile)
        controller.createChangeSQLITE3(attributes)
        attributes["description"] = "this is an updated description"
        attributes["author"] = "updated author"
        attributes["file"] = "updated file"
        #because there is an updated change id after the creation
        attributes["change_id"] = controller.commits[-1].toDict()["change_id"]
        controller.updateChangeSQLITE3(attributes)
        last_commit = controller.commits[-1].toDict()
        self.assertEquals(last_commit["description"],"this is an updated description")
        self.assertEquals(last_commit["author"],"updated author")
        self.assertEquals(last_commit["file"],"updated file")
    def testDeleteChange(self):
        """test for the deleting a change"""
        attrs = createAttributes()
        controller = commit_controller.controler(dbfile)
        controller.createChangeSQLITE3(attrs)
        change_id = getChangeID()
        controller.deleteChangeSQLITE3(change_id)
        lastChange = controller.commits[-1].toDict()
        expected = change_id -1
        actual = lastChange["change_id"]
        self.assertEqual(expected,actual)
clearTestDB()
unittest.main()