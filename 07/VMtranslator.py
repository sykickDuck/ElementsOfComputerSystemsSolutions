import sys
import os

class VMtranslator:
    '''Translates a single .vm file or directory containing .vm files in to an .asm file for the Hack Platform'''    
    
    def translate(self):
        """Function responsible for orchestrating the translation"""

        statusCode = None
        
        if (len(sys.argv) == 1):        
            print("No file provided...")
            statusCode = 2

        else:    
            path = sys.argv[1]
            
            if not os.path.exists(path):
                print("Provided File/Folder does not exist")
                statusCode = 2

        return statusCode


if __name__ == '__main__':
    translator = VMtranslator()
    translator.translate()