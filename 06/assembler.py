import os
import sys
from parser import Parser
from parser import CommandType
from code import *
from SymbolTable import SymbolTable

def main():
    
    if (len(sys.argv) == 1):        
        print("No file provided...")
    else:    
        path = sys.argv[1]
        
        if os.path.exists(path):
            fileName = __getFileName(path)

            if __getFileExtension(fileName) == "asm":
                print("Assembling: " + fileName)
                __assemble(path)

            else:
                print("Provided file is not an asm file")
        else:
            print("No file found...")

def __getFileName(path):
    return path.split("/")[-1]

def __getFileExtension(fileName):
    return fileName.split(".")[-1]

def __assemble(path): 

    symbolTable = __firstPass(path)
    __secondPass(path, symbolTable)

def __firstPass(path):

    symbolTable = SymbolTable()

    with Parser(path) as parser:
        currentRomAddress = 0

        while parser.hasMoreCommands():
            parser.advance()

            if parser.commandType() == CommandType.L_COMMAND:
                print("Adding symbol:" + parser.symbol() + " @ line:" + str(currentRomAddress))
                symbolTable.addEntry(parser.symbol(),currentRomAddress)
            else:
                currentRomAddress += 1

    return symbolTable

def __secondPass(path, symbolTable):
    
    currentRamAddress = 16

    with Parser(path) as parser:
        destination = __getFileName(path).split(".")[0] + ".hack"
        with open(destination, mode="w", encoding="utf-8") as hackFile:
            print("Destination: " + destination)

            while parser.hasMoreCommands():
                parser.advance()
                print ("Current command:" + parser.currentCommand)
                command = parser.commandType()

                if command == CommandType.A_COMMAND:                                        
                    symbol = parser.symbol()
                    addressAsInt = None
                    
                    if isInt(symbol): #treat as constant 
                        addressAsInt = int(symbol)                       
                    else:
                        if(symbolTable.contains(symbol)):
                            addressAsInt = symbolTable.getAddress(symbol)
                        else:
                            addressAsInt = currentRamAddress
                            symbolTable.addEntry(symbol,addressAsInt)
                            currentRamAddress += 1
                    
                    #Now write constant to file
                    addressAsBinary = "0" + "{0:015b}".format(addressAsInt) + "\n"
                    print("Writing constant to file:" + addressAsBinary)
                    hackFile.write(addressAsBinary) #prefix the constant with a 0 as per A-instruction

                elif command == CommandType.C_COMMAND:
                    instruction = "111" +   comp(parser.comp()) + dest(parser.dest()) + jump(parser.jump()) + "\n"
                    print("Writing instuction:" + instruction)
                    hackFile.write(instruction)
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    main()
    