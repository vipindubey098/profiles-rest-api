from django.contrib import admin

from profiles_api import models

# Register your models here.

admin.site.register(models.UserProfile) # this tells the django to register our user profile model with the admin side so it makes it accessible to admin interface
admin.site.register(models.ProfileFeedItem) # Next we gonna create a serializer for our profile feed item objects going to serializer.py
