from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class URLTests(TestCase):
    def test_homepageURL(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signupURL(self):
        response = self.client.get('/accounts/p00osignup/')
        self.assertEqual(response.status_code, 200)

    def test_loginURL(self):
        response = self.client.get('/accounts/p00ologin/')
        self.assertEqual(response.status_code, 200)

    def test_socialURL(self):
        response = self.client.get('/social/')
        self.assertEqual(response.status_code, 200)

    """"
    def test_profile(self):
        # need to figure out how to create a profile on this line then use it to test a profile URL
        
        # Something like...
        # user = create_user_profile("jferg", "John", "jferg0906@gmail.com")

        response = self.client.get('/profile/{0}/'.format(user.profile))
        self.assertEqual(response.status_code, 200)
    """
