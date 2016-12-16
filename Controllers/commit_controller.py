"""
Author: Samuel coombe
Description: class for controlling the data removing slight dependancies from the data
"""
import sqlite3
from Controllers import SQLite3Controller
from  Models import commit_model
from Controllers import project_controller
import logging
logger = logging.getLogger("commit_controller")
logger.setLevel(logging.INFO)

class controler():
    def __init__(self,dbname):
        """Initialisng the class takes a database location as a param"""
        logger.debug("commit_controller: controller: init: dbname: {}".format(dbname))
        self.dbname = dbname
        self.sqliteController = SQLite3Controller.controller(self.dbname)
        self.getChangesSQLITE3()

    def getChangesSQLITE3(self):
        """function for getting all of the changes from the db"""
        changes = self.sqliteController.DatabaseGet("SELECT * FROM change",{})
        commits_dict = {}
        commits = []
        #looping thorugh all of the results from the db
        for change in changes:
            change_id = change[0]
            project_id = change[1]
            file = change[2]
            author = change[3]
            description = change[4]
            date_of_change = change[5]
            logger.debug("commit_controller: controller: getChangeSQLITE3: getting a change: change_id:{}, project_id:{}, file:{}, author:{}, description:{}, date_of_change{}".format(change_id, project_id, file, author, description, date_of_change))
            #creating a new instance of the commit model changes class which is used for modeling.
            #dictionary for searching by id
            commits.append(commit_model.changes(change_id,project_id,file, author, description, date_of_change))
            commits_dict[str(change_id)] = commit_model.changes(change_id,project_id,file, author, description, date_of_change)
        self.commits_dict = commits_dict
        self.commits = commits




    def createChangeSQLITE3(self,attributes):
        """Adding a new change to the sqlite database
           taking atributes project id, file, author, date, description in a dictionary"""
        #this function is either returning an error string or True
        validAttrs = self.validateAttributes(attributes)
        logger.debug("commit_change: createChangeSQLITE: the valid attrs is returned: {}".format(str(validAttrs)))
        if validAttrs == True:
            self.getChangesSQLITE3();
            #creating the sql string to insert values into the database using the sqlite controller defined above
            self.sqliteController.DatabaseTransaction("INSERT INTO change (PROJECT_ID, FILE_PATH, AUTHOR,DESCRIPTION,DATE_OF_CHANGE)"
                         "VALUES(?, ?, ?, ?,?)",( int(attributes["project_id"]),attributes["file"],attributes["author"],attributes["description"],attributes["date_of_change"]))
            self.getChangesSQLITE3()
            validAttrs = True
        else:
            #updating the project atribute
            self.getChangesSQLITE3()
            #in this instane the validation is returning a error string
            return validAttrs
        self.getChangesSQLITE3()

        return True

    def updateChangeSQLITE3(self,attributes):
        """function for the udating one change
        takes a dictionary on attributes"""
        #this function returns True or an error string
        validAttrs = self.validateAttributes(attributes)
        if validAttrs:
            #calling the sqlite controller already defined in the ctor
            #takes *args and a query
            self.sqliteController.DatabaseTransaction("UPDATE change "
                                                      "SET PROJECT_ID = ?, "
                                                      "FILE_PATH = ?, "
                                                      "AUTHOR = ?,"
                                                      "DESCRIPTION = ?, "
                                                      "DATE_OF_CHANGE = ? "
                                                      "WHERE CHANGE_ID = ?",
                                                      (int(attributes["project_id"]), attributes["file"], attributes["author"], attributes["description"],
                      attributes["date_of_change"],attributes["change_id"]))
            #updating the changes.
            self.getChangesSQLITE3()
        else:
            #returing the error string in this instance
            return validAttrs
        return validAttrs

    def deleteChangeSQLITE3(self,change_id):
        valid = self.checkChangeID(change_id)
        logger.debug(":deleteChangeSQLITE3: deleteing a change: {}, Valid: {}".format(str(change_id),str(valid)))
        if valid == True:
            self.sqliteController.DatabaseTransaction("DELETE FROM change WHERE CHANGE_ID= ?",(change_id,))
        self.getChangesSQLITE3()
        return valid

    def checkChangeID(self,change_id):
        valid = False
        for change in self.commits:
            change = change.toDict()
            if change["change_id"] == change_id:
                valid = True
        return valid

    def checkProjectID(self,project_id):
        """function for checking that the project id passed into the create change is valid"""
        errorString = ""
        logger.debug("commit_controller: checkProjectID: checking for a valid projectID: {}".format(str(project_id)))
        control = project_controller.controller(self.dbname)
        projs = control.projects
        valid_project_id = False
        for proj in projs:
            proj = proj.toDict()
            if project_id == proj["project_id"]:
                logger.debug("commit_controller: checkProjectId: Found a valid ID: passed, {} = returned = {}".format(str(project_id),str(proj["project_id"])))
                valid_project_id = True
            logger.debug("commit_controller: checkProjectId: if valid: {}".format(str(valid_project_id == False)))
        if valid_project_id == False:
            logger.debug("commit_controller: checkProjectId: Returning error string")
            return "invalid project key"
        return True

    def validateAttributes(self, validate_attributes):
        """function for validating the project attributes"""
        errorString = ""
        validAttrs = True
        #passing  a list of objets into the length validation function
        validAttrs = self.lengthValidation([{"attr":validate_attributes["author"],"name":"author","upperbound":20,"lowerbound":0},
                                                   {"attr":validate_attributes["description"], "name":"description", "upperbound":240, "lowerbound":0},
                                                   {"attr":validate_attributes["file"],"name":"file","upperbound":30,"lowerbound":0},])
        valid = self.checkProjectID(validate_attributes["project_id"])
        logger.debug("commit_controller: validateAttribute: checkProjectId return: {}".format(str(valid)))
        logger.debug("commit_controller: validateAttribute: validProject_ID and valid attributes: {}".format(str(valid == True and validAttrs == True)))
        if valid == True and validAttrs == True:
            validAttrs = valid and validAttrs
            return  validAttrs
        else:
            errorString = "valid Attributes error: {} project id errors: {}".format(str(validAttrs), str(valid))
            logger.debug("commit_change: validateAttribute: returning error string: {}".format(errorString))
            return errorString

    def lengthValidation(self,validation):
        """takes a list of objects which have attr, name, upperbound, lowerbound"""
        Valid = True
        #valid attrs will return this string from the function
        error_string = ""
        for validate in validation:
            length = len(str(validate["attr"]))
            if length > validate["upperbound"] or length <= validate["lowerbound"]:
                #building the error string in the funciton
                error_string += self.buildErrorLenString(validate["name"],validate["lowerbound"],validate["upperbound"])
                Valid = False
        if Valid:
            error_string = "Valid attributes have been passed"
            return True
        else:
            return  error_string

    def buildErrorLenString(self,attribute, lowerBound, upperBound):
        """function for building an error with the incorrect length"""
        return "Error: "+ attribute +" is not the correct length must be between "+ lowerBound + "  and "+  upperBound + \
        " charectors\n"
