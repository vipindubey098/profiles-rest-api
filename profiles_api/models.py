from django.db import models
from django.contrib.auth.models import AbstractBaseUser  #import abstractbaseuser
from django.contrib.auth.models import PermissionsMixin  #import permissionmixin
# above two are the standard base classes that you need to use when overwriting or customizing the default django user model
from django.contrib.auth.models import BaseUserManager


# Create your models here.
# Creating user manager just above model:
class UserProfileManager(BaseUserManager): # we gonna inherit from base user manager which is the default manager model that comes with django
    """Manager for user profiles"""
    # The way managers work specify some functions that can be used to manipulate objects within the module that the manager is for.
    # So the first function that we need to create is the create underscore use a function, this is what the django CLI will use when creating user with the command line tool.
    
    def create_user(self, email, name, password=None): # If don't specify password it will be default to none because of the way the django password checking system works, non password won't work because it needs to be hash. So basically until you set a password you won't be able to authenticate with user.
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")
        # normalizing the email address, that means it will lowercase the first half of email address
        email = self.normalize_email(email)
        # Creating user model
        user = self.model(email=email, name=name) # it will create a new model that usermanager(UserProfileManager) is representing
        #we can't just pass the password above, we need to use set password function that comes with our user model so it is a part of abstractbase user  
        user.set_password(password) # password is encrypted we gonna make sure the password is converted to a hash and never stored as plain text in the db

        #save user
        user.save(using=self._db) # Standard procedure for daving data in db

        # Now we can return the user
        return user

    # Next function we need to create is to create super user function & this will use our create_user() function [Above created], but also assign superuser status

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""

        # we will use create_user function to create user
        user = self.create_user(email, name, password) # self is automatically pass in any class function

        # We haven't used is_superuser & is_staff in UserProfile class cox. permissionmixxin already have it
        user.is_superuser = True 
        user.is_staff = True
        user.save(using=self._db)

        return user





# Lets created a new class called Userprofile and inherit from the abstractbaseuser & permissionmixin base classes

class UserProfile(AbstractBaseUser, PermissionsMixin): # inheriting will help to customize it.
    """Database model for user in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # adding below permissions system
    is_active = models.BooleanField(default=True) # It can use to determine profile is activated or not, boolean holds on True or False value.
    is_staff = models.BooleanField(default=False) # It is use to determine it is staff user or if they can access to django admin

    # next we wanna specify model manager that we gonna use for objects and this is required because  we need to use our custom user model with django CLI. so django needs to have a custom manager for the user model so it knows how to create users.

    objects = UserProfileManager()

    # below this we need to add couple more fields to our class and this is for it again work with django admin and also the django authentication system

    USERNAME_FIELD = 'email'  # We are overriding default username field, which is normally called username. replacing it with our email feild.
    # so this means when we authenticate users instead of providing them a username and password they gonna provide email id and password.

    REQUIRED_FIELDS = ['name']

    # we need to give django ability to retrive the fullname of the user
    def get_full_name(self): # self because we are defining a function inside class we must specify self as the first argument. This default python convention.
        """ Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    # We literally just specifying these functions so that we can use integrate our custom user model with other components in django and because we don't have a way to specify a shorter name we're gonna return the same name as the full name and the last name we've kind of merged them both into single name field here.
    # Finally we need to specify these string representation of our model, Now this is the item that we want to retain when we convert a user profile object to a string:

    def __str__(self):
        """Return string representation of our user"""
        return self.email



