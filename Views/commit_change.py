import sqlite3
import time

import Controllers.project_controller
from Controllers import commit_controller
from Models import commit_model

"""
file to track change dates and why they occured
"""

"""
class for commiting changes
"""
class commit_change:
    def __init__(self,test):
        if(test):
            self.DB = "test.db"
        else:
            self.DB = "Changes.db"

    def viewLastChange(self):
        commits = commit_controller.getChangesSQLITE3()
        lastChange = commits[len(commits) - 1]
        print("Last change\nAuthor: " +lastChange.AUTHOR + "\nFile: " + lastChange.FILE + "\nDate of change: "\
              + lastChange.DATE_OF_CHANGE + "\nDescription: " + lastChange.DESCRIPTION)
        return lastChange

    """
    function for adding a new change
    """
    def addChange(self):
        projects = Controllers.project_controller.getProjectsSQLITE3()
        print("The current projects are: ")
        for projs in projects:
            proj = projs.toDict()
            print("project id: " + str(proj["project_id"]) + " project name: " + proj["project_name"] + ",")
        project_id = input("Enter the id of the project to use: ")
        author = input("Enter the author of the change: ")
        description = input("Enter the description of the change: ")
        # name of the file changed
        file = input("Enter the file that has been changed: ")
        # getting the time
        date = time.strftime('%d/%m/%y')
        # calling the add change to the database ading the attributes to a dictionary
        commit_controller.createChangeSQLITE3({"project_id": str(project_id), "author": author, "description": description,
                                               "file": file, "date_of_change": date},"Changes.db")


    """
    takes a string to add to a file, and the fileName
    """
    def addOrCreateChangeFile(self,changeString,changeFile):
        changeFile = open(changeFile, 'a')
        changeFile.write(changeString)

if __name__ == '__main__':
    comm_change = commit_change(False)
    exited = False
    functions = {"addChange","viewLastChange"}
    while not exited:
        for func in functions:
            print("The function: " + func + " Can be called")
        inp = input("Enter the function you would like to use Or 'EXIT'")
        if inp.upper() == "EXIT":
            exited = True
        elif inp.upper() == "ADDCHANGE":
            comm_change.addChange()
        elif inp.upper() == "VIEWLASTCHANGE":
            commit_change.viewLastChange()