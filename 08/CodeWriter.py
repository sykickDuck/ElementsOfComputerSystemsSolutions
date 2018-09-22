from Parser import CommandType

class CodeWriter:
    '''Responsible for writing VM commands as Hack assembly code to file'''

    segmentToRamBaseAddressLocation = {
        "local"     : "LCL",
        "argument"  : "ARG",
        "this"      : "THIS",
        "that"      : "THAT"
    }

    fixedRamSegment = {
        "pointer" : 3,
        "temp"    : 5,
    }


    def __init__(self, filePath):
        '''Set up writer to write assembly code to the specified file'''
        self.file = open(filePath, mode='w', encoding="utf-8")
        self.currentVmFile = None
        self.currentFileEqualityCheckCount = 0  #counts how many equality checks have occured during writing of the file
        self.currentFunctionName = None
        self.currentFunctionReturnLabelCount = 0

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def setFileName(self, fileName):
        '''Notify the code writer that new .VM file is being translated'''
        self.currentVmFile = fileName
        self.currentFileEqualityCheckCount = 0
        self.currentFunctionName = None
        self.currentFunctionReturnLabelCount = 0


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
            label = self.__getInternalEqualityLabel()
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
            label = self.__getInternalEqualityLabel()
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
            label = self.__getInternalEqualityLabel()
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
        
        if command == CommandType.C_PUSH:
            self.__writePush(segment, index)
        elif command == CommandType.C_POP:
            self.__writePop(segment, index)


    def __writePush(self, segment, index):
        '''push contents of segment[index] on to the stack'''
        if segment == 'constant':
            self.__writeAssembly("@{0}".format(int(index)))
            self.__writeAssembly("D=A")
            self.__writeAssembly("@SP") #rest of instruction to push reg d on to stack
            self.__writeAssembly("A=M")
            self.__writeAssembly("M=D")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M+1")
        elif segment in self.segmentToRamBaseAddressLocation:
            baseAddressLocation = self.segmentToRamBaseAddressLocation[segment]
            self.__writeAssembly("@{0}".format(int(index)))
            self.__writeAssembly("D=A")
            self.__writeAssembly("@{0}".format(baseAddressLocation))
            self.__writeAssembly("A=D+M")
            self.__writeAssembly("D=M")
            self.__writeAssembly("@SP") #rest of instructions to push reg d on to stack
            self.__writeAssembly("A=M")
            self.__writeAssembly("M=D")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M+1")
        elif segment in self.fixedRamSegment:
            address = (int(self.fixedRamSegment[segment])) + (int(index))
            self.__writeAssembly("@{0}".format(int(address)))
            self.__writeAssembly("D=M")
            self.__writeAssembly("@SP") #rest of instruction to push reg d on to stack
            self.__writeAssembly("A=M")
            self.__writeAssembly("M=D")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M+1")
        elif segment == 'static':
            self.__writeAssembly("@{0}.{1}".format(self.currentVmFile, index))
            self.__writeAssembly("D=M")
            self.__writeAssembly("@SP") #rest of instructions to push reg d on to stack
            self.__writeAssembly("A=M")
            self.__writeAssembly("M=D")
            self.__writeAssembly("@SP")
            self.__writeAssembly("M=M+1")


    def __writePop(self, segment, index):
        '''pop top of stack to segment[index]'''
        if segment in self.segmentToRamBaseAddressLocation:
            baseAddressLocation = self.segmentToRamBaseAddressLocation[segment]
            self.__writeAssembly("@{0}".format(baseAddressLocation)) #following lines work out where popping the stack to in ram and stores in R13
            self.__writeAssembly("D=M")
            self.__writeAssembly("@{0}".format(int(index)))
            self.__writeAssembly("D=D+A")
            self.__writeAssembly("@R13")
            self.__writeAssembly("M=D")
            self.__writeAssembly("@SP") #following lines pop stack into reg d
            self.__writeAssembly("M=M-1")
            self.__writeAssembly("A=M")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0") #end of pop into reg D
            self.__writeAssembly("@R13") #rest of commands takes contents of reg d and puts into location stored in R13
            self.__writeAssembly("A=M")
            self.__writeAssembly("M=D")
        elif segment in self.fixedRamSegment:
            address = (int(self.fixedRamSegment[segment])) + (int(index))
            self.__writeAssembly("@SP") #following lines pop stack into reg d
            self.__writeAssembly("M=M-1")
            self.__writeAssembly("A=M")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0")
            self.__writeAssembly("@{0}".format(int(address))) #following lines put contents of reg D into segment
            self.__writeAssembly("M=D")
        elif segment == 'static':
            self.__writeAssembly("@SP") #following lines pop stack into reg d
            self.__writeAssembly("M=M-1")
            self.__writeAssembly("A=M")
            self.__writeAssembly("D=M")
            self.__writeAssembly("M=0")
            self.__writeAssembly("@{0}.{1}".format(self.currentVmFile, index))
            self.__writeAssembly("M=D")


    def writeLabel(self, label):
        '''Writes assembly code for a VM label'''
        self.__writeAssembly("({0})".format(self.__buildLabelText(label)))


    def writeGoto(self, label):
        '''Writes assembly for goto label'''
        self.__writeAssembly("@{0}".format(self.__buildLabelText(label)))
        self.__writeAssembly("0;JMP")


    def writeIf(self, label):
        '''Writes assembly to goto a label based on the last command on the stack'''
        self.__writeAssembly("@SP")
        self.__writeAssembly("M=M-1")
        self.__writeAssembly("A=M")
        self.__writeAssembly("D=M")
        self.__writeAssembly("M=0")
        self.__writeAssembly("@{0}".format(self.__buildLabelText(label)))
        self.__writeAssembly("D;JNE")


    def writeFunction(self, functionName, numLocals):
        '''Writes assembly to declare the start of a function'''
        self.currentFunctionName = functionName
        self.currentFunctionReturnLabelCount = 0
        functionInitLoopLabel = "{0}${1}".format(functionName, "FunctionInit")

        self.__writeAssembly("({0})".format(functionName)) #Function Label           
        self.__writeAssembly("@R13") #Initialise register for loop
        self.__writeAssembly("M=0")
        self.__writeAssembly("({0}.Begin)".format(functionInitLoopLabel)) #Start of loop
        self.__writeAssembly("@{0}".format(numLocals))
        self.__writeAssembly("D=A")
        self.__writeAssembly("@R13")
        self.__writeAssembly("D=D-M")
        self.__writeAssembly("@{0}.End".format(functionInitLoopLabel))
        self.__writeAssembly("D;JLE")
        self.__writeAssembly("@LCL")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@R13")
        self.__writeAssembly("A=D+M")
        self.__writeAssembly("M=0")
        self.__writeAssembly("@R13")
        self.__writeAssembly("M=M+1")
        self.__writeAssembly("@{0}.Begin".format(functionInitLoopLabel))
        self.__writeAssembly("0;JMP")
        self.__writeAssembly("({0}.End)".format(functionInitLoopLabel))
        self.__writeAssembly("@{0}".format(numLocals))
        self.__writeAssembly("D=A")
        self.__writeAssembly("@SP")
        self.__writeAssembly("M=D+M")

    def writeCall(self, functionName, numArgs):
        '''Writes assembly code that effects the call command'''
        returnLabel = "{0}$RetLbl.{1}".format(self.currentFunctionName, self.currentFunctionReturnLabelCount)
        self.currentFunctionReturnLabelCount +=1
        self.__writeAssembly("@{0}".format(returnLabel)) #push return label, LCL, ARG, THIS, THAT
        self.__writeAssembly("D=A")
        self.__writeAssembly("@SP")
        self.__writeAssembly("A=M")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@SP")
        self.__writeAssembly("M=M+1")
        self.__writePushPointerOnToStack("LCL")
        self.__writePushPointerOnToStack("ARG")
        self.__writePushPointerOnToStack("THIS")
        self.__writePushPointerOnToStack("THAT")
        self.__writeAssembly("@SP") #reposition ARG to SP-numArgs-5
        self.__writeAssembly("D=M")
        self.__writeAssembly("@5")
        self.__writeAssembly("D=D-A")
        self.__writeAssembly("@{0}".format(numArgs))
        self.__writeAssembly("D=D-A")
        self.__writeAssembly("@ARG")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@SP") #Reposition LCL to SP
        self.__writeAssembly("D=M")
        self.__writeAssembly("@LCL")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@{0}".format(functionName)) #goto function code
        self.__writeAssembly("0;JMP")
        self.__writeAssembly("({0})".format(returnLabel))


    def __writePushPointerOnToStack(self, pointer):
        '''writes assembly to push the pointer specified in the label on to the stack'''
        self.__writeAssembly("@{0}".format(pointer))
        self.__writeAssembly("D=M")
        self.__writeAssembly("@SP")
        self.__writeAssembly("A=M")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@SP")
        self.__writeAssembly("M=M+1")


    def writeReturn(self):
        '''Write assembly for a function return'''
        self.__writeAssembly("@LCL") #FRAME=LCL
        self.__writeAssembly("D=M")
        self.__writeAssembly("@R13")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@R13") #RET = FRAME-5
        self.__writeAssembly("D=M")
        self.__writeAssembly("@5")
        self.__writeAssembly("A=D-A")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@R14")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@SP") #ARG = pop
        self.__writeAssembly("A=M-1")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@ARG")
        self.__writeAssembly("A=M")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@ARG") #SP = ARG+1
        self.__writeAssembly("D=M+1")
        self.__writeAssembly("@SP")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@R13")#THAT = FRAME-1
        self.__writeAssembly("M=M-1")
        self.__writeAssembly("A=M")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@THAT")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@R13")#THIS = FRAME-2
        self.__writeAssembly("M=M-1")
        self.__writeAssembly("A=M")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@THIS")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@R13")#ARG = FRAME-3
        self.__writeAssembly("M=M-1")
        self.__writeAssembly("A=M")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@ARG")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@R13") #LCL = FRAME-4
        self.__writeAssembly("M=M-1")
        self.__writeAssembly("A=M")
        self.__writeAssembly("D=M")
        self.__writeAssembly("@LCL")
        self.__writeAssembly("M=D")
        self.__writeAssembly("@R14") #goto RET
        self.__writeAssembly("A=M")
        self.__writeAssembly("0;JMP")
        
    def writeInit(self):
        '''Writes Assembly for bootstrapping the program'''
        self.__writeAssembly("@256")
        self.__writeAssembly("D=A")
        self.__writeAssembly("@SP")
        self.__writeAssembly("M=D")
        self.writeCall("Sys.init", "0")

    def __getInternalEqualityLabel(self):
        '''Generates a label for use in internal equality checks'''
        label = "{0}$Eq.{1}".format(self.currentFunctionName, self.currentFileEqualityCheckCount)
        self.currentFileEqualityCheckCount +=1 
        return label

    def __buildLabelText(self, label):
        '''To reduce repeating code of writing labels'''
        return "{0}${1}".format(self.currentFunctionName, label)

    def __writeAssembly(self, asm):
        self.file.write(asm + "\n")


    def close(self):
        '''Closes the file'''
        self.file.close()