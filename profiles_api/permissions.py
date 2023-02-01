from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit there own profile"""
    #The way you define permission classes is you add a has object permissions function to the class which gets called every time a request is made to the API that we assign our permission to the class. This function returns true or false, To determine whether the authenticated use has the permission to do the change they are trying to do.

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id # if evaluate then true or it will through false
    # Every time request is made the django rest framework will call this function has object permission and it will pass in the request, view, actual objects that we are checking the permissions against.
    # So when we try and update a user profile this gets called and all of these functions get passed then
    # So when the user makes a request we're going to check if the request is in the safe methods. If it isn't safe methods we're just gonna allow the request to go through. Otherwise if it's not in the safe method so they're using an update or delete or something like that we will return the result of the obj.id = request.user.id. This way it will return true or false depend on user trying to update on profile or others. This is custom permissions.


# Cannot assign "<django.contrib.auth.models.AnonymousUser object at 0x7f9069f7d1d0>": "ProfileFeedItem.user_profile" must be a "UserProfile" instance. -> if we are getting an error like this we will fix it using permission

# We gonna add a new permission class which will be similar to UpdateOwnProfile() class which is above, so this permission class gonna ensure that if a user is updating a status that is assigned to that user account, This user can update their own feed items in the db.

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own profile"""
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id

# Now we need to configure our view set to use this permission. To do that go to views.py