import unittest
from unittest.mock import patch, mock_open
from Parser import Parser

class ParserTests(unittest.TestCase):


    def setUpFilePatchWith(self, read_data):
        patcher = patch('Parser.open', new_callable=mock_open, read_data= read_data)
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


    def test_fileWhereFirstCommandNotOnFirstLineHasCommand(self):
        '''OBJECTIVE: Test that parser recognises a file where first command is not on the first line'''
        self.setUpFilePatchWith("//Push 2 on to the stack \n push 2")
        self.assertEqual(True, self.translator.hasMoreCommands(), "A file with a command should return true")


    def test_currentCommandStartsAtNone(self):
        '''OBJECTIVE: Test that current command is none initially'''
        self.setUpFilePatchWith("push 2")
        self.assertIsNone(self.translator.currentCommand, "Parser should initialise with current command at None")


    def test_advanceSetsCurrentCommand(self):
        '''OBJECTIVE: Test that advance sets current command to next command'''
        command = "push 2"
        self.setUpFilePatchWith(command)
        self.translator.advance()
        self.assertEqual(command, self.translator.currentCommand, "Advance should change current command")


    def test_advanceRemovesWhiteSpacePaddingCommand(self):
        '''OBJECTIVE: Test that advance removes whitespace around command when setting current command'''
        command = "push 2"
        self.setUpFilePatchWith(" " + command + " ")
        self.translator.advance()
        self.assertEqual(command, self.translator.currentCommand, "Surrounding white space should be removed")


    def test_advanceRemovesCommentsOnLine(self):
        '''OBJECTIVE: Test that advance removes comments found on same line as command'''
        command = "push 2"
        self.setUpFilePatchWith(command + "    //push 2 on to stack")
        self.translator.advance()
        self.assertEqual(command, self.translator.currentCommand, "Comments should be removed for current command")

    #Test current fails due to seek and tell methods of the mock object not acting as I expected
    def test_hasMoreCommandsMaintainsCurrentStreamPosition(self):
        '''OBJECTIVE: Test that calling hasMoreCommands does not move the file stream forward'''
        self.setUpFilePatchWith("push 2")
        self.translator.hasMoreCommands()
        self.assertTrue(self.translator.hasMoreCommands(), "hasMoreCommands() should not change the position in the stream")


if __name__ == "__main__":
    unittest.main()