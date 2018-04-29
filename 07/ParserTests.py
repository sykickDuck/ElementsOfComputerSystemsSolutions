import unittest
from unittest.mock import patch, mock_open
from Parser import Parser

class ParserTests(unittest.TestCase):


    def setUpFilePatchWith(self, read_data):
        patcher = patch('builtins.open', new_callable=mock_open, read_data= read_data)
        self.addCleanup(patcher.stop)
        self.mock_file = patcher.start()
        self.translator = Parser("mockFile.vm")


    def test_emptyFileHasNoCommands(self):
        '''OBJECTIVE: Test that Parser recognises an empty file has no more commands'''
        self.setUpFilePatchWith("")
        self.assertEqual(False, self.translator.hasMoreCommands(), "Empty file should return false for has more commands")


    def test_fileWithABlankLineHasNoCommands(self):
        '''OBJECTIVE: Test that parser recognises that a blank line is not a command'''
        self.setUpFilePatchWith("\n")
        self.assertEqual(False, self.translator.hasMoreCommands(), "File with a blank line should return false for has more commands")


    def test_fileWithOnlyCommentHasNoCommands(self):
        '''OBJECTIVE: Test that parser recognises a file with only a comment has no more commands'''
        self.setUpFilePatchWith("//File on has a comment")
        self.assertEqual(False, self.translator.hasMoreCommands(), "A file with only a comment should return false")


    def test_fileWithSingleCommandHasCommand(self):
        '''OBJECTIVE: Test that parser recognises a file with a command has more commands'''
        self.setUpFilePatchWith("push 2")
        self.assertEqual(True, self.translator.hasMoreCommands(), "A file with a command should return true")


    @patch("builtins.open", new_callable=mock_open, read_data="//Push 2 on to the stack \n push 2")
    def test_fileWhereFirstCommandNotOnFirstLineHasCommand(self, mock):
        '''OBJECTIVE: Test that parser recognises a file where first command is not on the first line'''
        self.setUpFilePatchWith("//Push 2 on to the stack \n push 2")
        self.assertEqual(True, self.translator.hasMoreCommands(), "A file with a command should return true")


if __name__ == "__main__":
    unittest.main()