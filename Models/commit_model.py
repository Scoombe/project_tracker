"""model of the changes in the changes.db """
class changes:
    def __init__(self,change_id,project_id,file,author,description,date_of_change):
        self.CHANGE_ID = change_id
        self.PROJECT_ID = project_id
        self.FILE = file
        self.DESCRIPTION = description
        self.AUTHOR = author
        self.DATE_OF_CHANGE = date_of_change
    def toDict(self):
        dict = {"change_id": self.CHANGE_ID, "project_id": self.PROJECT_ID, "file": self.FILE,
                "author":self.AUTHOR, "description":self.DESCRIPTION, "date_of_change":self.DATE_OF_CHANGE}
        return dict