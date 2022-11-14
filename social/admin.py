# Imports
from django.contrib import admin
from .models import Post, UserProfile

# Registers the post to the database
admin.site.register(Post)

# Registers users profile to the database
admin.site.register(UserProfile)


