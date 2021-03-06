import sys
import os
import glob
from Parser import Parser, CommandType
from CodeWriter import CodeWriter

class VMtranslator:
    '''Translates a single .vm file or directory containing .vm files in to an .asm file for the Hack Platform'''    
    
    def translate(self):
        '''Function responsible for orchestrating the translation'''

        #Following code for determining arguments and file/dir existence may need to be refactored out
        #However, not sure yet so will wait till further in development to make decision
        
        statusCode = None
        
        if (len(sys.argv) == 1):
            print("No file provided...")
            statusCode = 2

        else:    
            path = sys.argv[1]
            
            if not os.path.exists(path):
                print("Provided File/Folder does not exist")
                statusCode = 2
            else:   
                asmFileLocation = "{0}.asm".format(self.__getFileName(path).split('.')[0])

                with CodeWriter(asmFileLocation) as writer:
                    
                    writer.writeInit()
                    paths = []

                    if os.path.isdir(path):
                        paths = glob.glob("{0}/*.vm".format(path))
                    else:
                        paths.append(path)
                    
                    for currentPath in paths:
                        currentFileName = self.__getFileName(currentPath).split('.')[0]
                        writer.setFileName(currentFileName)
                        with Parser(currentPath) as parser:
                            while (parser.hasMoreCommands()):
                                parser.advance()
                                commandType = parser.commandType()
                                if commandType == CommandType.C_PUSH:
                                    writer.writePushPop(commandType, parser.arg1(), parser.arg2())
                                elif commandType == CommandType.C_POP:
                                    writer.writePushPop(commandType, parser.arg1(), parser.arg2())
                                elif commandType == CommandType.C_ARITHMETIC:
                                    writer.writeArithmetic(parser.arg1())
                                elif commandType == CommandType.C_LABEL:
                                    writer.writeLabel(parser.arg1())
                                elif commandType == CommandType.C_GOTO:
                                    writer.writeGoto(parser.arg1())
                                elif commandType == CommandType.C_IF:
                                    writer.writeIf(parser.arg1())
                                elif commandType == CommandType.C_FUNCTION:
                                    writer.writeFunction(parser.arg1(), parser.arg2())
                                elif commandType == CommandType.C_CALL:
                                    writer.writeCall(parser.arg1(), parser.arg2())
                                elif commandType == CommandType.C_RETURN:
                                    writer.writeReturn()



        return statusCode

    def __getFileName(self, path):
        splitString = list(filter(None, path.split("/")))
        return splitString[-1]

if __name__ == '__main__':
    '''Entry point for the VMtranslator.py file.  Responsible for bootstrapping the translation process'''
    translator = VMtranslator()
    translator.translate()