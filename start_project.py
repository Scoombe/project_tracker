import time
def main():
    """
    Function for the easy creation of project files, with built in comments and date and purpose
    No dependencies
    """
    #getting the date in the format date month year
    date = time.strftime('%d/%m/%y')
    fString = input("Enter the file name: ")
    author = input("Enter the author: ")
    purpose = input("Enter the purpose of the python file: ")
    language = input("Enter the lanaguage of the file: ")
    #the extensino
    extension = input("Enter the extension E.g if you want a .py then type py E.T.C: ")
    fileName = fString + "." + extension
    #opening the project file
    Projfile = open(fileName,'w')
    #building the project string
    ProjectString = "\"\"\"\n" \
                    "Author: "+author + "\n" \
                    "Function of the file: "+purpose+ "\n" \
                    "Date of creation: "+date + "\n"\
                    "Language: " + language +"\n"\
                    "\"\"\""
    Projfile.write(ProjectString)
    Projfile.close()

main()