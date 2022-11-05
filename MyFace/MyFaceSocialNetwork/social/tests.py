from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from .models import UserProfile, Post
# Create your tests here.
'''
password = 'password'
test_admin = User.objects.create_superuser('testuser', 'testuser@gmail.com', password)
c = Client()
c.login(username=test_admin.username, password=password)

\
class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(author=UserProfile)
        Post.objects.create(body="12")

    def test_user_created(self):
        post = Post.objects.filter(name="12")
        self.assertTrue(post.exist())
'''