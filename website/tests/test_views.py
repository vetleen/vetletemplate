from django.test import TestCase
from django.urls import reverse
from django.test import Client

from django.contrib.auth.models import User

# Create your tests here.
class TestTheUrls(TestCase):
    """
    Test that URLs yield expected response
    """
    def test_url_status(self):
        """
        TEST THAT URLS EXIST
        """
        ## Set the conditions for URL-testing
        self.urls_to_test = [
            '/',
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/password_change',
            '/accounts/password_change/done',
            '/accounts/password_reset',
            '/accounts/password_reset/done',
            '/accounts/reset/done',
            '/sign-up/',
            '/change-password/'
            ]
        self.acceptable_url_statuses = [200, 302]

        #test that URLs exist
        for url in self.urls_to_test:
            response = self.client.get(url, follow=True)
            self.assertIn(response.status_code, self.acceptable_url_statuses)

class FrontPageTest(TestCase):
    @classmethod
    def set_up_test_data(self):
        pass
    #test that the correct template is used
    def test_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class LoginTest(TestCase):
    @classmethod
    def set_up_test_data(self):
        pass
    #test that the correct template is used
    def test_view_uses_correct_template(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
