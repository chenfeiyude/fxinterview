from django.test import TestCase
from ..code_executor import fx_python_executor, fx_java_executor, fx_js_executor, fx_php_executor
import logging


class FXPythonCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = """
def hello():
    print('Hello World')

hello()
        """
        results = fx_python_executor.run_code(code)
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
        results = fx_java_executor.run_code(code)
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
        results = fx_js_executor.run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")

        hello = results['output']
        self.assertEqual(hello(), "Hello World")


class FXPHPCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = """
        <?php
        echo "Hello World";
        ?> 
        """
        results = fx_php_executor.run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")
        self.assertEqual(results['output'].strip().replace('\n', ''), "Hello World")
