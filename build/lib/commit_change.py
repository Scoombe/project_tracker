import time
"""
function to track change dates and why they occured
"""
def main():
    author  = input("Enter the author of the change: ")
    description = input("Enter the description of the change: ")
    #name of the file changed
    file = input("Enter the file that has been changed: ")
    #getting the time
    date= time.strftime('%d/%m/%y')
    changeFile = open("changes.txt",'a')
    changeString = "===================================="\
                    "File changed: " + file + ""\
                    "Author of the change: " + author + ""\
                    "Description of the change: "+ description + ""\
                    "Date of the change: "+date + ""
    changeFile.write(changeString)

def viewLastChange():
    changeEnd = False
    change = []
    reversed = reverseFile("changes.txt")
    while changeEnd == False:
        for line in reversed:
            # checking if the line conatains an equals the end of a change
            if stringContains(line, "="):
                changeEnd = True
            if changeEnd == False:
                change.append(line)
    for line in change:
        print(line)

    return change


def stringContains(line,char):
    """looking for a charector in a string
    boolean function"""
    print(len(line))
    for i in range(1,len(line)):
        if line[i] == char:
            print("found an : " + line[i] + " charecter")
            return True
    return False

def reverseFile(file):
    """Returning a list of the reversed file"""
    reverse = []
    count = 0
    for line in reversed(list(open(file, 'r'))):
        reverse.append(line)
    return reverse

viewLastChange()