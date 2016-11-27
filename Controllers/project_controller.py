import sqlite3

from Models import project_model

"""
Getting the projects from the projects table
uses SQLITE3
"""
class controller():
    def __init__(self,dbname):
        self.dbname = dbname
        #updating the self.projects attr
        self.getProjectsSQLITE3()
    """
    Function for getting all of the projects from the database
    """
    def getProjectsSQLITE3(self):
        conn = sqlite3.connect(self.dbname)
        projs = conn.execute("SELECT * FROM project")
        attributes = {}
        projects = []
        for proj in projs:
            attributes["project_id"] = proj[0]
            attributes["author"] = proj[1]
            attributes["description"] = proj[2]
            attributes["date_of_creation"] = proj[3]
            attributes["language"] = proj[4]
            attributes["project_name"] = proj[5]
            project = project_model.projects(attributes)
            projects.append(project)
        self.projects = projects
    """
    function for creating a new project
    """
    def createProjectSQLITE3(self, attributes):
        #updating the project list everytime there is a new project created
        self.getProjectsSQLITE3()
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        project_id = 1
        # getting the change id by selecting all of the changes and plussing 1 to the id
        for project in self.projects:
            proj = project.toDict()
            if proj["project_id"] >= project_id:
                project_id = int(proj["project_id"]) + 1
        # creating the sql string to insert values into the database
        c.execute("INSERT INTO project "
                  "VALUES(?, ?, ?, ?, ?, ?)", (
                  project_id, attributes["author"], attributes["description"],
                  attributes["date_of_creation"], attributes["language"], attributes["name"]))
        conn.commit()
        conn.close()
        self.getProjectsSQLITE3()
        return True