from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.


class ApplicationViewTestCase(TestCase):

    def test_not_found(self):
        """Test if no email sent and the view return 404 not found error"""
        url = reverse("main:view_application_questions",
                      kwargs={'application_question_id':1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 404)