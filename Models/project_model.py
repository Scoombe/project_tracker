"""Projects model"""
class projects:
    def __init__(self, projectAttrs):
        self.PROJECT_ID = projectAttrs["project_id"]
        self.PROJECT_NAME = projectAttrs["project_name"]
        self.AUTHOR = projectAttrs["author"]
        self.DESCRIPTION = projectAttrs["description"]
        self.DATE_OF_CREATION = projectAttrs["date_of_creation"]
        self.LANGUAGE = projectAttrs["language"]
    """
    Function for returning the model to a dictionary
    """
    def toDict(self):
        return {"project_id":self.PROJECT_ID, "project_name":self.PROJECT_NAME,"author":self.AUTHOR,
                "description":self.DESCRIPTION, "date_of_creation":self.DATE_OF_CREATION, "language": self.LANGUAGE}