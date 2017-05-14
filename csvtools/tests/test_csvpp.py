import io
import sys
import unittest
import os
import time
# from .. import csvpp
# from ..utils import InputError


class TestPrintRow(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()
        self.new_stdout = io.StringIO()
        self.new_stderr = io.StringIO()
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr

    def tearDown(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        pass

    def test_csvpp_1(self):
        f_correct = open('./data/testfile_output_csvpp_1','r')
        os.system('python ./csvtools/csvpp.py ./data/testfile_input_1 -o ./data/output')
        f = open('./data/output','r')
        self.assertEqual(f.read(), f_correct.read())
        f.close()

    def test_csvpp_2(self):
        f_correct = open('./data/testfile_output_csvpp_2','r')
        os.system('python ./csvtools/csvpp.py ./data/testfile_input_2 -o ./data/output')
        f = open('./data/output','r')
        self.assertEqual(f.read(), f_correct.read())
        f.close()
