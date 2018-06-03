from Parser import CommandType

class CodeWriter:
    '''Responsible for writing VM commands as Hack assembly code to file'''


    def __init__(self, filePath):
        '''Set up writer to write assembly code to the specified file'''
        self.file = open(filePath, mode='w', encoding="utf-8")
        self.currentVmFile = None


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def setFileName(self, fileName):
        '''Notify the code writer that new .VM file is being translated'''
        self.currentVmFile = fileName


    def writeArithmetic(self, command):
        '''Write assembly code for the provided arithmetic command to the file'''
        if(command == "add"):
            self.__writeAssembly("@SP")
            self.__writeAssembly("A=M")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0")
            self.__writeAssembly("A=A-1")
            self.__writeAssembly("M=D+M")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M-1")


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