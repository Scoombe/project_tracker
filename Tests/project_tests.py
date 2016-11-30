import sys
import os.path
#adding the files to the sys path that are in the diretory above, so that if the test is run directly
#you will be able to see the modules from the directory above.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Controllers import project_controller
import time
import sqlite3
import unittest
db_file = os.path.realpath('../project_startup/Data/test.db')

def clearTestDB():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("DELETE FROM project;")
    conn.commit()
    conn.close()

def createProjectsqlite3test():
    attritbutes = {}
    attritbutes["author"] = "Samuel Coombe"
    attritbutes["description"] = "new project for testing the project controller"
    attritbutes["date_of_creation"]  = time.strftime('%d/%m/%y')
    attritbutes["language"] = "python"
    attritbutes["name"] = "testProject"
    controller = project_controller.controller(db_file)
    controller.createProjectSQLITE3(attritbutes)
    #getting the last project
    projs = controller.projects[len(controller.projects) - 1].toDict()
    return {"actual":projs,
            "expected":{"project_id":1, "project_name":attritbutes["name"],
                        "author":attritbutes["author"],"description":attritbutes["description"],
                        "date_of_creation":attritbutes["date_of_creation"],
                        "language": attritbutes["language"]}
            }
class commitChangeTest(unittest.TestCase):
    def testCreate(self):
        """test for creating a project in the test database"""
        result = createProjectsqlite3test()
        self.assertEqual(result["expected"],result["actual"])

clearTestDB()
unittest.main()