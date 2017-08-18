import os, sys, logging
from django.test import TestCase
from ..compiler import fx_python_compiler
from ..utils import fx_file_utils


class FXPythonCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = 'print(1*2)'
        results = fx_python_compiler.run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")
        self.assertEqual(results['output'], "2\n")
