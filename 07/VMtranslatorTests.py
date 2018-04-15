import unittest
from unittest.mock import patch
from VMtranslator import VMtranslator
import sys

class VMtranslatorTests(unittest.TestCase):

    def test_NoCommandLineArgumentErrorCodeTwo(self):
        args = ["VMtranslator.py"] #args will always contain at least the script being executed
        
        with patch.object(sys,'argv',args):
            translator = VMtranslator()
            code = translator.translate()
            
        self.assertEqual(2, code, "Translator is expected to exit with error code 2.")

    @patch("os.path")
    def test_BadFilePathErrorCodeTwo(self, mock_path):
        args = ["Vmtranslator.py", "BadFilePath.py"]
        mock_path.exists.return_value = False

        with patch.object(sys,'argv',args):
            translator = VMtranslator()
            code = translator.translate()
            
        self.assertEqual(2, code, "Translator is expected to exit with error code 2.")

if __name__ == "__main__":
    unittest.main()