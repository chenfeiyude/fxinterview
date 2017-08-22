from django.test import TestCase
from ..compiler import fx_python_compiler, fx_java_compiler, fx_js_compiler
import logging

class FXPythonCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = """
def hello():
    print('Hello World')

hello()
        """
        results = fx_python_compiler.run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")
        self.assertEqual(results['output'], "Hello World\n")


class FXJavaCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = """
        public class hello {
            public static void main(String []args) {
                System.out.println("Hello World");
            }
        }
        """
        results = fx_java_compiler.run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")
        self.assertEqual(results['output'], "Hello World\n")


class FXJSCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = """
        function hello(){
            var test = "Hello World";
            return test;
        }
        """
        results = fx_js_compiler.run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")

        hello = results['output']
        self.assertEqual(hello(), "Hello World")
