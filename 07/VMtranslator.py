import sys
import os

class VMtranslator:
    '''Translates a single .vm file or directory which contains .vm files in to an .asm file for the Hack Platform'''    
    
    def translate(self):
        """Function responsible for orchestrating the translation"""
        
        if (len(sys.argv) == 1):        
            print("No file provided...")
            return 2

        else:    
            path = sys.argv[1]
            
            if not os.path.exists(path):
                return 2


if __name__ == '__main__':
    translator = VMtranslator()
    translator.translate()