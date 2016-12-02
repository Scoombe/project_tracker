"""
Author: Samuel coombe
Description: class for controlling the data removing slight dependancies from the data
"""
import sqlite3
from Controllers import SQLite3Controller
from  Models import commit_model
from Controllers import project_controller


class controler():
    def __init__(self,dbname):
        """Initialisng the class takes a database location as a param"""
        self.dbname = dbname
        self.getChangesSQLITE3()
        self.sqliteController = SQLite3Controller.controller(self.dbname)
    def getChangesSQLITE3(self):
        """function for getting all of the changes from the db"""
        changes = self.sqliteController.DatabaseGet("SELECT * FROM change")
        commits_dict = {}
        commits = []
        #looping thorugh all of the results from the db
        for change in changes.fetchall():
            change_id = change[0]
            project_id = change[1]
            file = change[2]
            author = change[3]
            description = change[4]
            date_of_change = change[5]
            #creating a new instance of the commit model changes class which is used for modeling.
            #dictionary for searching by id
            commits.append(commit_model.changes(change_id,project_id,file, author, description, date_of_change))
            commits_dict[str(change_id)] = commit_model.changes(change_id,project_id,file, author, description, date_of_change)
        self.commits_dict = commits_dict
        self.commits = commits




    def createChangeSQLITE3(self,attributes):
        """Adding a new change to the sqlite database
           taking atributes project id, file, author, date, description in a dictionary"""
        validAttrs = False
        if self.checkProjectID(attributes["project_id"]):
            self.getChangesSQLITE3();
            #creating the sql string to insert values into the database using the sqlite controller defined above
            self.sqliteController.DatabaseTransaction("INSERT INTO change (PROJECT_ID, FILE_PATH, AUTHOR,DESCRIPTION,DATE_OF_CHANGE)"
                         "VALUES(?, ?, ?, ?,?)",( int(attributes["project_id"]),attributes["file"],attributes["author"],attributes["description"],attributes["date_of_change"]))
            self.getChangesSQLITE3()
            validAttrs = True
        else:
            self.getChangesSQLITE3()
        return validAttrs

    def updateChangeSQLITE3(self,attributes):
        """function for the udating one change
        takes a dictionary on attributes"""
        validAttrs = False
        if self.checkProjectID(attributes["project_id"]):
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
            validAttrs = True
        return validAttrs
    def checkProjectID(self,project_id):
        """function for checking that the project id passed into the create change is valid"""
        control = project_controller.controller(self.dbname)
        projs = control.projects
        valid_project_id = False
        for proj in projs:
            proj = proj.toDict()
            if project_id == proj["project_id"]:
                valid_project_id = True
        return  valid_project_id
