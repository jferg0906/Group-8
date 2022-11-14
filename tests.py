from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import admin
from social.models import Post

# Create your tests here.

class Tests(TestCase):
    def test_homepageURL(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signupURL(self):
        response = self.client.get('/accounts/p00osignup/')
        self.assertEqual(response.status_code, 200)

    def test_loginURL(self):
        response = self.client.get('/accounts/p00ologin/')
        self.assertEqual(response.status_code, 200)

    def test_admin(self):
        user = User.objects.create_superuser(username="test", password="12345")
        login = self.client.login(username="test", password="12345")
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_deny_regular_user_to_adminURL(self):
        user = User.objects.create_user(username="test", password="12345")
        login = self.client.login(username="test", password="12345")
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_socialURL(self):
        response = self.client.get('/social/')
        self.assertEqual(response.status_code, 200)
        
    def test_create_user(self):
        user = User.objects.create_user(username="test", password="12345")
        assert User.objects.filter(username="test").exists()
        
    def test_create_user_and_log_in(self):
        user = User.objects.create_user(username="test", password="12345")
        login = self.client.login(username="test", password="12345")
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_profileURL(self):
        user = User.objects.create_user(username="test", password="12345")
        login = self.client.login(username="test", password="12345")
        response = self.client.get('/social/profile/{0}/'.format(user.pk))
        self.assertEqual(response.status_code, 200)

    def test_multiple_profiles(self):
        user = User.objects.create_user(username="test1", password="12345")
        assert User.objects.filter(pk=user.pk).exists()
        
        user = User.objects.create_user(username="test2", password="12345")
        assert User.objects.filter(pk=user.pk).exists()
        
        user = User.objects.create_user(username="test3", password="12345")
        assert User.objects.filter(pk=user.pk).exists()

    def test_profile_editURL(self):
        user = User.objects.create_user(username="test", password="12345")
        login = self.client.login(username="test", password="12345")
        response = self.client.get('/social/profile/edit/{0}/'.format(user.pk))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        user = User.objects.create_user(username="test", password="12345")
        post = Post.objects.create(author = user)
        assert Post.objects.filter(pk=post.pk).exists()

    def test_multiple_posts(self):
        user = User.objects.create_user(username="test", password="12345")
        post = Post.objects.create(author = user)
        assert Post.objects.filter(pk=post.pk).exists()

        post = Post.objects.create(author = user)
        assert Post.objects.filter(pk=post.pk).exists()

        post = Post.objects.create(author = user)
        assert Post.objects.filter(pk=post.pk).exists()

    def test_postURL(self):
        user = User.objects.create_user(username="test", password="12345")
        post = Post.objects.create(author = user)
        login = self.client.login(username="test", password="12345")
        response = self.client.get('/social/post/{0}/'.format(user.pk))
        self.assertEqual(response.status_code, 200)

    def test_post_editURL(self):
        user = User.objects.create_user(username="test", password="12345")
        post = Post.objects.create(author = user)
        response = self.client.get('/social/post/edit/{0}/'.format(post.pk))
        self.assertEqual(response.status_code, 200)

    def test_post_deleteURL(self):
        user = User.objects.create_user(username="test", password="12345")
        post = Post.objects.create(author = user)
        response = self.client.get('/social/post/delete/{0}/'.format(post.pk))
        self.assertEqual(response.status_code, 200)

    def test_search_nothingURL(self):
        user = User.objects.create_user(username="test", password="12345")
        response = self.client.get('/social/search/?query=')
        self.assertEqual(response.status_code, 200)

    def test_search_userURL(self):
        user = User.objects.create_user(username="test", password="12345")
        response = self.client.get('/social/search/?query=test')
        self.assertEqual(response.status_code, 200)