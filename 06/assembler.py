import os
import sys
from parser import Parser
from parser import CommandType
from code import *

def main():
    #try:
    
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
    
    #except IndexError:
    #    print("No arguments passed!")

def __getFileName(path):
    return path.split("/")[-1]

def __getFileExtension(fileName):
    return fileName.split(".")[-1]

def __assemble(path): 

    destination = __getFileName(path).split(".")[0] + ".hack"

    with Parser(path) as parser:
        with open(destination, mode="w", encoding="utf-8") as hackFile:
            print("Destination: " + destination)

            while parser.hasMoreCommands():
                parser.advance()
                command = parser.commandType()

                if command == CommandType.A_COMMAND:
                    symbol = parser.symbol()
                    address = "0" + "{0:015b}".format(int(symbol)) + "\n"
                    print("Writing constant to file:" + address)
                    hackFile.write(address) #prefix the constant with a 0 as per A-instruction
                elif command == CommandType.C_COMMAND:
                    instruction = "111" +   comp(parser.comp()) + dest(parser.dest()) + jump(parser.jump()) + "\n"
                    print("Writing instuction:" + instruction)
                    hackFile.write(instruction)

if __name__ == '__main__':
    main()
    