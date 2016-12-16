import sys
import os.path
#adding the files to the sys path that are in the diretory above, so that if the test is run directly
#you will be able to see the modules from the directory above.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Controllers import project_controller
import time
import sqlite3
import unittest
import logging
db_file = os.path.realpath('../project_startup/Data/test.db')

logger = logging.getLogger("project_tests")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def clearTestDB():
    logger.debug("project_tests: ClearTestDB: Clearing the tests so they are as they are before")
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("DELETE FROM project;")
    conn.commit()
    conn.close()

def getProjectId():
    """function for getting the last project_id"""
    """getting the last change from the commit controller"""
    project_id = 1
    # getting the change id from the test database
    conn = sqlite3.connect(db_file)
    # the sql for getting the right data
    projects = conn.execute("SELECT PROJECT_ID FROM project")
    # looping round all of the returned rows from the database
    for project in projects.fetchall():
        if project[0] >= project_id:
            project_id = project[0]
    logger.debug("project_tests: getProjectID: getting a poroject ID to use in the tests: {}".format(str(project_id)))
    return project_id

def createAttrs():
    attributes = {}
    attributes["author"] = "Samuel Coombe"
    attributes["description"] = "new project for testing the project controller"
    attributes["date_of_creation"] = time.strftime('%d/%m/%y')
    attributes["language"] = "python"
    attributes["name"] = "testProject"
    logger.debug("project_tests: createAttrs: creating valid attrs to use in testing: {}".format(str(attributes)))
    return  attributes

def createProjectsqlite3test():
    attritbutes = createAttrs()
    controller = project_controller.controller(db_file)
    controller.createProjectSQLITE3(attritbutes)
    #getting the last project
    projs = controller.projects[- 1].toDict()
    logger.debug("project_tests: createProjectSQLlite3test: Cerating a new change using the project_controller: {}".format(str(projs)))
    return {"actual":projs,
            "expected":{"project_id":getProjectId(), "project_name":attritbutes["name"],
                        "author":attritbutes["author"],"description":attritbutes["description"],
                        "date_of_creation":attritbutes["date_of_creation"],
                        "language": attritbutes["language"]}
            }
class commitChangeTest(unittest.TestCase):
    def testCreate(self):
        """test for creating a project in the test database"""
        result = createProjectsqlite3test()
        self.assertEqual(result["expected"],result["actual"])
    def testUpdate(self):
        """testing the updating of an existing project"""
        attrs = createAttrs()
        controller = project_controller.controller(db_file)
        controller.createProjectSQLITE3(attrs)
        attrs["name"] = "updated project name"
        attrs["description"] = "updated description"
        attrs["project_id"] = getProjectId()
        controller.updateProjectSQLITE3(attrs)
        proj = controller.projects[-1].toDict()
        logger.debug("project_test: testUpdate: testing an update occurs: updated attrs, {}: actual attrs, {}".format(str(attrs), str(proj)))
        self.assertEqual(attrs["name"], proj["project_name"])
        self.assertEqual(attrs["description"], proj["description"])
    def testDeleteProject(self):
        """todo add delete project"""
        project_id = getProjectId()
        attrs = createAttrs()
        controller = project_controller.controller(db_file)
        attrs["description"] = "this is a deleted project"
        attrs["author"] = "deleted"
        controller.createProjectSQLITE3(attrs)
        project_id = getProjectId()
        controller.deleteProjectSQLITE3(getProjectId())
        projs = controller.projects[-1].toDict()
        actual = projs["project_id"]
        expected = project_id -1
        self.assertEqual(expected, actual)

clearTestDB()
unittest.main()