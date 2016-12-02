import sqlite3

from Models import project_model
from Controllers import SQLite3Controller
"""
Getting the projects from the projects table
uses SQLITE3
"""
class controller():
    def __init__(self,dbname):
        self.dbname = dbname
        self.sqlite_controller = SQLite3Controller.controller(dbname)
        #updating the self.projects attr
        self.getProjectsSQLITE3()
    """
    Function for getting all of the projects from the database
    """
    def getProjectsSQLITE3(self):
        conn = sqlite3.connect(self.dbname)
        projs = self.sqlite_controller.DatabaseGet("SELECT * FROM project")
        attributes = {}
        projects = []
        projectDict = {}
        for proj in projs:
            attributes["project_id"] = proj[0]
            attributes["author"] = proj[1]
            attributes["description"] = proj[2]
            attributes["date_of_creation"] = proj[3]
            attributes["language"] = proj[4]
            attributes["project_name"] = proj[5]
            project = project_model.projects(attributes)
            projects.append(project)
            projectDict[attributes["project_id"]] = project
        self.projects = projects
        self.projectDict = projectDict

    def createProjectSQLITE3(self, attributes):
        """function for creating a new project"""
        #updating the project list everytime there is a new project created
        validAttrs = False
        self.getProjectsSQLITE3()
        # creating the sql string to insert values into the database
        self.sqlite_controller("INSERT INTO project(AUTHOR, DESCIPTION, DATE_OF_CREATION, LANGUAGE, NAME) "
                  "VALUES(?, ?, ?, ?, ?)", (
                  attributes["author"], attributes["description"],
                  attributes["date_of_creation"], attributes["language"], attributes["name"]))
        self.getProjectsSQLITE3()
        validAttrs = True
        return validAttrs
    def validateAttributes(self, attributes):
        """function for validating the project attributes"""
        #TODO finish vallidate attributes
    def updateProjectSQLITE3(self, attributes):
        """function for updating a project with sqlite3"""
