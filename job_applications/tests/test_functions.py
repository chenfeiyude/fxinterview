from django.test import TestCase
from ..code_executor.fx_executor_factory import FXExecutorFactory, ExecutorLanguage
from main.utils import fx_constants
import logging


class FXExecutorFactoryTestCase(TestCase):

    def test_get_executor(self):

        self.assertEquals(ExecutorLanguage.python, ExecutorLanguage[fx_constants.LANGUAGE_PYTHON])
        self.assertIsNotNone(FXExecutorFactory.get_executor(ExecutorLanguage.python))
        self.assertIsNotNone(FXExecutorFactory.get_executor(fx_constants.LANGUAGE_PYTHON))

class FXPythonCompilerTestCase(TestCase):

    def test_run_code(self):
        """Test if run code methods return the expected results"""
        code = """
def hello():
    print('Hello World')

hello()
        """
        results = FXExecutorFactory.get_executor(fx_constants.LANGUAGE_PYTHON).run_code(code)
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
        results = FXExecutorFactory.get_executor(fx_constants.LANGUAGE_JAVA).run_code(code)
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
        results = FXExecutorFactory.get_executor(fx_constants.LANGUAGE_JAVASCRIPT).run_code(code)
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
        results = FXExecutorFactory.get_executor(fx_constants.LANGUAGE_PHP).run_code(code)
        self.assertIsNotNone(results)
        self.assertEqual(results['code'], "Success")
        self.assertEqual(results['output'].strip().replace('\n', ''), "Hello World")
