class model():
    def toDict(self):
        dictionairy = {}
        """looping through of the definitions in the dir of this class"""
        for attr in dir(self):
            if not callable(attr) and not attr.startswith("__") and not attr == "toDict":
                """getting tthe lower case name of attr"""
                dictionairy[str(attr).lower()] = getattr(self,attr)
        return dictionairy

                