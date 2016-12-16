import sqlite3
import logging

from Models import project_model
from Controllers import SQLite3Controller
logger = logging.getLogger("project_controller")
logger.setLevel(logging.INFO)
#creating a new console handler
ch = logging.StreamHandler()
#logging debug to the console
ch.setLevel(logging.INFO)
#changing the formatt
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#setting the new formatter
ch.setFormatter(formatter)
#adding it to the logger
logger.addHandler(ch)

"""
Getting the projects from the projects table
uses SQLITE3
"""
class controller():
    def __init__(self,dbname):
        logger.debug("init: initializing the controller: {}".format(str(dbname)))
        self.dbname = dbname
        self.sqlite_controller = SQLite3Controller.controller(dbname)
        #updating the self.projects attr
        self.getProjectsSQLITE3()

    def getProjectsSQLITE3(self):
        """Function for getting all of the projects from the database"""
        conn = sqlite3.connect(self.dbname)
        #getting the projects from the sqlite controller
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
            logger.debug("getProjectSQLITE3: getting the projects form the sql: {}".format(str(project.toDict())))
            projects.append(project)
            projectDict[attributes["project_id"]] = project
        self.projects = projects
        self.projectDict = projectDict

    def createProjectSQLITE3(self, attributes):
        """function for creating a new project"""
        #updating the project list everytime there is a new project created
        valid = self.validateAttributes(attributes)
        logger.debug("createProjectSQLITE3: creating a new project: {}: validAttrs: {}".format(str(attributes),str(valid)))
        if valid == True:
            self.getProjectsSQLITE3()
            # creating the sql string to insert values into the database
            self.sqlite_controller.DatabaseTransaction("INSERT INTO project(AUTHOR, DESCRIPTION, DATE_OF_CREATION, LANGUAGE, NAME) "
                      "VALUES(?, ?, ?, ?, ?)", (
                      attributes["author"], attributes["description"],
                      attributes["date_of_creation"], attributes["language"], attributes["name"]))
            self.getProjectsSQLITE3()
            return True
        else:
            return valid

    def updateProjectSQLITE3(self, attributes,):
        """function for updating a project with sqlite3"""
        valid = self.validateAttributes(attributes)
        logger.debug("updateProjectSQLITE3: updating a project from the attrs: {}: valid attrs: {}".format(str(attributes),str(valid)))
        if valid == True:
            self.sqlite_controller.DatabaseTransaction("UPDATE project " +
                                   "SET AUTHOR=?, DESCRIPTION =?, DATE_OF_CREATION=?, LANGUAGE=?, NAME=? " +
                                   "WHERE PROJECT_ID=?",((attributes["author"]),attributes["description"],attributes["date_of_creation"],
                                   attributes["language"],attributes["name"],attributes["project_id"]))
        self.getProjectsSQLITE3()
        return valid

    def deleteProjectSQLITE3(self,project_id):
        """Function for deleting an existing project"""
        valid = self.checkProjectID(project_id)
        logger.debug("deleteProjectSQLITE3: deleting a project: passed project id: {}, valid: {}".format(str(project_id),str(valid)))
        if valid == True:
            self.sqlite_controller.DatabaseTransaction("DELETE FROM project WHERE PROJECT_ID =?;", (project_id,))
        self.getProjectsSQLITE3()
        return valid

    def checkProjectID(self,project_id):
        """function for checking that the passed project id exists and can be used."""
        valid = False
        for project in self.projects:
            project = project.toDict()
            if project["project_id"] == project_id:
                valid = True
        if valid == False:
            return "incorect project id"
        return valid

    def validateAttributes(self, attributes):
        """function for validating the project attributes"""
        #passing  a list of objets into the length validation function
        validAttrs = self.lengthValidation([{"attr":attributes["author"],"name":"author","upperbound":20,"lowerbound":0},
                                                   {"attr":attributes["description"], "name":"description", "upperbound":240, "lowerbound":0},
                                                   {"attr":attributes["language"],"name":"language","upperbound":40,"lowerbound":0},
                                                   {"attr":attributes["name"],"name":"name","upperbound":50,"lowerbound":0}])
        return validAttrs

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
            return Valid
        return error_string

    def buildErrorLenString(self,attribute, lowerBound, upperBound):
        """function for building an error with the incorrect length"""
        return "Error: "+ attribute +" is not the correct length must be between "+ lowerBound + "  and "+  upperBound + \
        " charectors\n"