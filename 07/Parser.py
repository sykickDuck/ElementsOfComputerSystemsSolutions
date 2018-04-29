from enum import Enum

class CommandType(Enum):
    C_ARITHMETIC = 0
    C_PUSH       = 1
    C_POP        = 2
    C_LABEL      = 3
    C_GOTO       = 4
    C_IF         = 5
    C_FUNCTION   = 6
    C_RETURN     = 7
    C_CALL       = 8


class Parser:
    '''Responsible for parsing a single .VM file'''

    commandWords = {
        "push"     : CommandType.C_PUSH,
        "pop"      : CommandType.C_POP,
        "add"      : CommandType.C_ARITHMETIC,
        "sub"      : CommandType.C_ARITHMETIC,
        "neg"      : CommandType.C_ARITHMETIC,
        "eq"       : CommandType.C_ARITHMETIC,
        "gt"       : CommandType.C_ARITHMETIC,
        "lt"       : CommandType.C_ARITHMETIC,
        "and"      : CommandType.C_ARITHMETIC,
        "or"       : CommandType.C_ARITHMETIC,
        "not"      : CommandType.C_ARITHMETIC,
        "label"    : CommandType.C_LABEL,
        "goto"     : CommandType.C_GOTO,
        "if"       : CommandType.C_IF,
        "function" : CommandType.C_FUNCTION,
        "return"   : CommandType.C_RETURN,
        "call"     : CommandType.C_CALL,
    }

    def __init__(self, filePath):
        ''''Set up parser to read the specified file'''
        self.file = open(filePath, encoding="utf-8")
        self.currentCommand = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


    def hasMoreCommands(self):
        '''The file has more commands to parse'''

        #after seeking next command move file stream position back
        currentPosition = self.file.tell()
        commandFound = self.__seekNextCommand() != None
        self.file.seek(currentPosition)

        return commandFound


    def advance(self):
        '''Advance the parser to the next commands'''
        self.currentCommand = self.__seekNextCommand()


    def __seekNextCommand(self):
        '''Seeks the next command in the file'''
        commandFound = False
        currentline = None
        nextCommand = None

        while currentline != "" and commandFound == False:
            currentline = self.file.readline()
            commandFound = (currentline != "\n" and currentline[0:2] != "//" and currentline != "")

        if(commandFound):
            currentLineStrippedOfComments = currentline.split("//")[0]
            nextCommand = currentLineStrippedOfComments.strip()

        return nextCommand


    def commandType(self):
        '''Type of command parser is currently on'''
        commandWord = self.currentCommand.split(" ")[0]

        return self.commandWords[commandWord]


    def arg1(self):
        '''Returns first argument of the current command'''
        arg1 = None

        if(self.commandType() == CommandType.C_ARITHMETIC):
            arg1 = self.currentCommand.split(" ")[0]
        else:
            self.currentCommand.split(" ")[1]

        return arg1


    def arg2(self):
        '''Returns the second argument of the current command'''
        return self.currentCommand.split(" ")[2]
