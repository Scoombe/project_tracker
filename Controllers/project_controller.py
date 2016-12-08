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

    def getProjectsSQLITE3(self):
        """Function for getting all of the projects from the database"""
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
        valid, errorString = self.validateAttributes(attributes)
        if valid:
            self.getProjectsSQLITE3()
            # creating the sql string to insert values into the database
            self.sqlite_controller.DatabaseTransaction("INSERT INTO project(AUTHOR, DESCRIPTION, DATE_OF_CREATION, LANGUAGE, NAME) "
                      "VALUES(?, ?, ?, ?, ?)", (
                      attributes["author"], attributes["description"],
                      attributes["date_of_creation"], attributes["language"], attributes["name"]))
            self.getProjectsSQLITE3()
            return True
        else:
            return valid, errorString

    def updateProjectSQLITE3(self, attributes):
        """function for updating a project with sqlite3"""
        valid, errorString = self.validateAttributes(attributes)
        if not valid:
            self.sqlite_controller("UPDATE project "
                                   "SET AUTHOR=?, DESCRIPTION =?,DATE_OF_CREATION=?,LANGUAGE=?,NAME=?",attributes)
            self.getProjectsSQLITE3()
            return True
        else:
            return False, errorString

    def validateAttributes(self, attributes):
        """function for validating the project attributes"""
        errorString = ""
        validAttrs = True
        #passing  a list of objets into the length validation function
        validAttrs, error = self.lengthValidation([{"attr":attributes["author"],"name":"author","upperbound":20,"lowerbound":0},
                                                   {"attr":attributes["description"], "name":"description", "upperbound":240, "lowerbound":0},
                                                   {"attr":attributes["language"],"name":"language","upperbound":40,"lowerbound":0},
                                                   {"attr":attributes["name"],"name":"name","upperbound":50,"lowerbound":0}])
        return validAttrs, errorString

    def lengthValidation(self,validation):
        """takes a list of objects which have attr, name, upperbound, lowerbound"""
        Valid = True
        #valid attrs will return this string from the function
        error_string = ""
        for valid in validation:
            length = len(str(valid["attr"]))
            if length > valid["upperbound"] or length <= valid["lowerbound"]:
                #building the error string in the funciton
                error_string += self.buildErrorLenString(valid["name"],valid["lowerbound"],valid["upperbound"])
                Valid = False
        if valid:
            error_string = "Valid attributes have been passed"
        return error_string, Valid

    def buildErrorLenString(self,attribute, lowerBound, upperBound):
        """function for building an error with the incorrect length"""
        return "Error: "+ attribute +" is not the correct length must be between "+ lowerBound + "  and "+  upperBound + \
        " charectors\n"