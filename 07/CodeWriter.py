from Parser import CommandType

class CodeWriter:
    '''Responsible for writing VM commands as Hack assembly code to file'''

    def __init__(self, filePath):
        '''Set up writer to write assembly code to the specified file'''
        self.file = open(filePath, mode='w', encoding="utf-8")
        self.currentVmFile = None
        self.currentFileEqualityCheckCount = 0  #counts how many equality checks have occured during writing of the file


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def setFileName(self, fileName):
        '''Notify the code writer that new .VM file is being translated'''
        self.currentVmFile = fileName
        self.currentFileEqualityCheckCount = 0


    def writeArithmetic(self, command):
        '''Write assembly code for the provided arithmetic command to the file'''
        if command == "add":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=D+M")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "sub":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("D=-D")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=D+M")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "neg":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=-M")
        elif command == "eq":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("D=-D")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=D+M")
            self.__writeAssembly("M=0") #Make assumption equality will be false
            label = "{0}.EqualityJump.{1}".format(self.currentVmFile, self.currentFileEqualityCheckCount)
            self.currentFileEqualityCheckCount +=1
            self.__writeAssembly("@{0}".format(label))
            self.__writeAssembly("D;JNE")
            self.__writeAssembly("@SP") #Following lines before label find where the result of equality check is and sets it to be true
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=-1")
            self.__writeAssembly("({0})".format(label))
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "gt":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("D=-D")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=D+M")
            self.__writeAssembly("M=0") #Make assumption equality will be false
            label = "{0}.EqualityJump.{1}".format(self.currentVmFile, self.currentFileEqualityCheckCount)
            self.currentFileEqualityCheckCount +=1
            self.__writeAssembly("@{0}".format(label))
            self.__writeAssembly("D;JLE")
            self.__writeAssembly("@SP") #Following lines before label find where the result of equality check is and sets it to be true
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=-1")
            self.__writeAssembly("({0})".format(label))
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "lt":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("D=-D")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=D+M")
            self.__writeAssembly("M=0") #Make assumption equality will be false
            label = "{0}.EqualityJump.{1}".format(self.currentVmFile, self.currentFileEqualityCheckCount)
            self.currentFileEqualityCheckCount +=1
            self.__writeAssembly("@{0}".format(label))
            self.__writeAssembly("D;JGE")
            self.__writeAssembly("@SP") #Following lines before label find where the result of equality check is and sets it to be true
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=-1")
            self.__writeAssembly("({0})".format(label))
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "and":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=D&M")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "or":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=D|M")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")
        elif command == "not":
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=!M")


    def writePushPop(self, command, segment, index):
        '''Write the assembly for the provided push/pop command to the file'''
        
        if command == CommandType.C_PUSH and segment == 'constant':
            self.__writeAssembly("@{0}".format(int(index)))
            self.__writeAssembly("D=A")
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("M=D")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M+1")


    def __writeAssembly(self, asm):
        self.file.write(asm + "\n")


    def close(self):
        '''Closes the file'''
        self.file.close()