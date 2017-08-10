from django.test import TestCase
from ..forms import JobForm


# Create your tests here.
class JobFormTest(TestCase):
    def test_forms_valid(self):
        valid_form_data = {'name': 'fake job 1', 'description': 'fake description 1'}
        valid__form = JobForm(data=valid_form_data)
        self.assertTrue(valid__form.is_valid())

    def test_forms_invalid(self):
        in_valid_form_data = {'name': '', 'description': 'fake description 1'}
        in_valid__form = JobForm(data=in_valid_form_data)
        self.assertFalse(in_valid__form.is_valid())
