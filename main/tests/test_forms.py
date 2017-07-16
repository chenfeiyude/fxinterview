from django.test import TestCase
from ..forms import CreateJobForm


# Create your tests here.
class CreateJobFormTest(TestCase):
    def test_forms_valid(self):
        valid_form_data = {'name': 'fake job 1', 'description': 'fake description 1'}
        valid__form = CreateJobForm(data=valid_form_data)
        self.assertTrue(valid__form.is_valid())

    def test_forms_invalid(self):
        in_valid_form_data = {'name': '', 'description': 'fake description 1'}
        in_valid__form = CreateJobForm(data=in_valid_form_data)
        self.assertFalse(in_valid__form.is_valid())
