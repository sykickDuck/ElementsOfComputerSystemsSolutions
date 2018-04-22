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
        commandFound = False
        currentline = None

        while currentline != "" and commandFound == False:
            currentline = self.file.readline()
            commandFound = (currentline != "\n" and currentline[0:2] != "//" and currentline != "")

        return commandFound

    def advance(self):
        '''Advance the parser to the next commands'''
        pass


    def commandType(self):
        '''Type of command parser is currently on'''
        return None


    def arg1(self):
        '''Returns first argument of the current command'''
        return ""


    def arg2(self):
        '''Returns the second argument of the current command'''
        return ""
