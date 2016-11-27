"""
Author: Samuel coombe
Description: class for controlling the data removing slight dependancies from the data
"""
import sqlite3
from  Models import commit_model
from Controllers import project_controller

class controler():
    def __init__(dbname,self):
        self.dbname = dbname
        self.changes = self.getChangesSQLITE3()
    """
    Function for getting all of the changes from the live sqlite database
    """
    def getChangesSQLITE3(self):
        conn = sqlite3.connect(self.dbname)
        changes = conn.execute("SELECT * FROM change")
        commits = []
        for change in changes.fetchall():
            change_id = change[0]
            project_id = change[1]
            file = change[2]
            author = change[3]
            description = change[4]
            date_of_change = change[5]
            commits.append(commit_model.changes(change_id,project_id,file, author, description, date_of_change))
        return commits
        conn.close()
    """
    Commiting the changes to database.
    Takes a list of commit_model objects. Takes the dbname parameter
    Deleting the changes then adding new ones.
    """
    def commitChangeSQLITE3(changes,dbname,self):
        #a test dbname can be passed into the database
        conn = sqlite3.connect(dbname)
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
    def createChangeSQLITE3(attributes,dbname,self):
        if checkProjectID(dbname, attributes["project_id"]):
            conn = sqlite3.connect(dbname)
            c = conn.cursor()
            changes = self.getChangesSQLITE3()
            change_id = 1
            #getting the change id by selecting all of the changes and plussing 1 to the id
            for change in changes:
                chng = change.toDict()
                if chng["change_id"] >= change_id:
                    change_id = int(chng["change_id"]) + 1
            #creating the sql string to insert values into the database
            c.execute("INSERT INTO change "
                         "VALUES(?, ?, ?, ?, ?,?)",(change_id, int(attributes["project_id"]),attributes["file"],attributes["author"],attributes["description"],attributes["date_of_change"]))
            conn.commit()
            conn.close()
            return True
        else:
            return False

"""
functino for checking that the project id passed into the create change is valid
"""
def checkProjectID(dbname, project_id):
    conn = sqlite3.connect(dbname)
    changes = conn.execute("SELECT * FROM project")
    valid_project_id = False
    for change in changes.fetchall():
        if project_id == change[0]:
            valid_project_id = True

    return  valid_project_id
