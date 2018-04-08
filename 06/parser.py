from enum import Enum

class CommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2


class Parser:

    def __init__(self, filePath):
        self.filePath = filePath
        self.file = open(self.filePath, encoding="utf-8")
        #setup the current line and the next line
        self.currentCommand = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def hasMoreCommands(self):

        #seek the next command then reset filestream to current place
        currentPosition = self.file.tell()
        commandFound = self.__seekNextCommand() != None
        self.file.seek(currentPosition)
        
        return commandFound

    def advance(self):
      self.currentCommand = self.__seekNextCommand()      

    #seeks the next command in the file and returns it
    def __seekNextCommand(self):
        commandFound = False
        currentline = None
        nextCommand = None

        while currentline != "" and commandFound == False:
            currentline = self.file.readline()
            commandFound = (currentline != "\n" and currentline[0:2] != "//" and currentline != "")
        
        if commandFound:
            currentLineWithNoComments = currentline.split("//")[0]
            nextCommand = currentLineWithNoComments.strip()

        return nextCommand

    def commandType(self):
        commandType = None
        
        if self.currentCommand[0] == "@":
            commandType = CommandType.A_COMMAND
        elif self.currentCommand [0] == "(" and self.currentCommand[-1] == ")":
            commandType = CommandType.L_COMMAND
        else:
            commandType = CommandType.C_COMMAND

        return commandType

    def symbol(self):

        if self.commandType() == CommandType.A_COMMAND:
            return self.currentCommand[1:]
        else:
            return self.currentCommand[1:-1]

    def dest(self):
        
        if("=" in self.currentCommand):
            return self.currentCommand.split("=")[0]
        else:
            return "null"

    def comp(self):
        
        comp = self.currentCommand

        if("=" in comp):
            comp = comp.split("=")[1]

        if(";" in comp):
            comp = comp.split(";")[0]
        
        return comp

    def jump(self):
        if(";" in self.currentCommand):
            return self.currentCommand.split(";")[1]
        else:
            return "null"


    