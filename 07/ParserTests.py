import unittest
from unittest.mock import patch, mock_open
from Parser import Parser

class ParserTests(unittest.TestCase):


    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_emptyFileHasNoCommands(self, mock):
        '''OBJECTIVE: Test that Parser recognises an empty file has no more commands'''

        translator = Parser("mockFile.vm")

        self.assertEqual(False,translator.hasMoreCommands(), "Empty file should return false for has more commands")

    @patch("builtins.open", new_callable=mock_open, read_data="\n")
    def test_fileWithABlankLineHasNoCommands(self, mock):
        '''OBJECTIVE: Test that parser recognises that a blank line is not a command'''

        translator = Parser("mock")
        self.assertEqual(False,translator.hasMoreCommands(), "File with a blank line should return false for has more commands")

    @patch("builtins.open", new_callable=mock_open, read_data="//File on has a comment")
    def test_fileWithOnlyCommentHasNoCommands(self, mock):
        '''OBJECTIVE: Test that parser recognises a file with only a comment has no more commands'''

        translator = Parser("mockFile.vm")
        self.assertEqual(False, translator.hasMoreCommands(), "A file with only a comment should return false")


    @patch("builtins.open", new_callable=mock_open, read_data="push 2")
    def test_fileWithSingleCommandHasCommand(self, mock):
        '''OBJECTIVE: Test that parser recognises a file with a command has more commands'''

        translator = Parser("mockFile.vm")
        self.assertEqual(True, translator.hasMoreCommands(), "A file with a command should return true")

    @patch("builtins.open", new_callable=mock_open, read_data="//Push 2 on to the stack \n push 2")
    def test_fileWhereFirstCommandNotOnFirstLineHasCommand(self, mock):
        '''OBJECTIVE: Test that parser recognises a file where first command is not on the first line'''

        translator = Parser("mockFile.vm")

        self.assertEqual(True, translator.hasMoreCommands(), "A file with a command should return true")

if __name__ == "__main__":
    unittest.main()