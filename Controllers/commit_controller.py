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
        self.dbname = dbname
        self.getChangesSQLITE3()
        self.sqliteController = SQLite3Controller.controller(self.dbname)
    """
    Function for getting all of the changes from the live sqlite database
    """
    def getChangesSQLITE3(self):
        conn = sqlite3.connect(self.dbname)
        changes = conn.execute("SELECT * FROM change")
        commits_dict = {}
        commits = []
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
        conn.close()
        self.commits_dict = commits_dict
        self.commits = commits



    """
    Commiting the changes to database.
    Takes a list of commit_model objects. Takes the dbname parameter
    Deleting the changes then adding new ones.
    """
    def commitChangeSQLITE3(self,changes):
        #a test dbname can be passed into the database
        conn = sqlite3.connect(self.dbname)
        create  = conn.cursor()
        project = conn.cursor()
        project.execute("SELECT * FROM PROJECT")

        sqlStr = "INSERT INTO change VALUES"
        #changes is a list of the change objects
        #building the insert string
        for change in changes:
            sqlStr = sqlStr + "("
            #foreach of the attribute
            for atr in  change.toDict:
                sqlStr = sqlStr + atr + ", "
            sqlStr = sqlStr + ")"
        sqlStr = sqlStr + (";")
        commit = create.execute("INSERT INTO change" + sqlStr)
        conn.save()
        conn.close()
    """
    Adding a new change to the sqlite database
    taking atributes project id, file, author, date, description in a dictionary
    """
    def createChangeSQLITE3(self,attributes):
        if self.checkProjectID(attributes["project_id"]):
            self.getChangesSQLITE3()
            #connection string for the sqlite connection
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()
            #creating the sql string to insert values into the database
            c.execute("INSERT INTO change (PROJECT_ID, FILE_PATH, AUTHOR,DESCRIPTION,DATE_OF_CHANGE)"
                         "VALUES(?, ?, ?, ?,?)",( int(attributes["project_id"]),attributes["file"],attributes["author"],attributes["description"],attributes["date_of_change"]))
            conn.commit()
            conn.close()
            self.getChangesSQLITE3()
            return True
        else:
            self.getChangesSQLITE3()
            return False

    def updateChangeSQLITE3(self,attributes):
        """
        function for the udating one change
        takes a dictionary on attributes
        """
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
            return True
        else:
            return False
    """
    functino for checking that the project id passed into the create change is valid
    """
    def checkProjectID(self,project_id):
        control = project_controller.controller(self.dbname)
        projs = control.projects
        valid_project_id = False
        for proj in projs:
            proj = proj.toDict()
            if project_id == proj["project_id"]:
                valid_project_id = True
        return  valid_project_id
