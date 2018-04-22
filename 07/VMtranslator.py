import sys
import os

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

        return statusCode


if __name__ == '__main__':
    '''Entry point for the VMtranslator.py file.  Responsible for bootstrapping the translation process'''
    translator = VMtranslator()
    translator.translate()