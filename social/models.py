# Imports
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime, now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Model for a post
class Post(models.Model):
    # Text that is entered when sharing a post
    shared_body = models.TextField(blank=True, null=True)
    # Original post text contents
    body = models.TextField()
    # When was the post created
    created_on = models.DateTimeField(default=localtime(now()))
    # When was the post shared
    shared_on = models.DateTimeField(blank=True, null=True)
    # Who is the post author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Who was the shared post author
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    # Likes on the post
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    # How to order post feed
    class Meta:
        ordering = ['-created_on', '-shared_on']


# Model for a user profile
class UserProfile(models.Model):
    # Users ID
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    # Users name
    name = models.CharField(max_length=30, verbose_name='name', null=True)
    # Users bio
    bio = models.TextField(max_length=500, blank=True)
    # Users birth date
    birth_date = models.DateField(null=True, blank=True)
    # Users location
    location = models.CharField(max_length=100, blank=True, null=True)
    # Users profile picture
    picture = models.ImageField(upload_to='uploads/profile_pictures/', default='uploads/profile_pictures/default.png', blank=True)
    # Users friends
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    # Users friend request
    friend_request = models.ManyToManyField(User, blank=True, related_name='friend_request')


# Creates and saves a users profile in the database
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # References the user objects stated in UserProfile
        UserProfile.objects.create(user=instance)


# Saves updates to the users profile in the database
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Saves profile instance
    instance.profile.save()


# Model for commenting on a post
class Comment(models.Model):
    # Comments text contents
    comment = models.TextField()
    # When was the comment created
    created_on = models.DateTimeField(default=timezone.now)
    # What post is this comment on
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # Comments author
    author = models.ForeignKey(User, on_delete=models.CASCADE)

