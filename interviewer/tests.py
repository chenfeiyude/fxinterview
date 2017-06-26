import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Company

# Create your tests here.


class CompanyModelTests(TestCase):

    def test_case_example(self):
        """
        describe your test case in here
        """
        company = Company(name="test")
        self.assertIs(company.name == "test", True)