from rest_framework import serializers

from profiles_api import models

#We will create a new class called hello serializers
class HelloSerializer(serializers.Serializer):
    """Serialzers a new field for testing our APIView"""
    # we're gonna create a simple serializer name input, an then we gonna us it to test the post functionality of out APIView, These function is similar to django forms
    # Define the serializer and then you specify the fields that you wanna accept in serializer the input
    # Serializers also take care of validation rules, if you want to accept a certain field of a certain type this will make sure that the content pass the API is of the correct type that you want to require the field
    name = serializers.CharField(max_length=10)


# The serializer that we gonna add here is gonna be a model serializer. It is very similar to regular serializer except it has a bunch of extra functionality which makes it easy to work with existing django db models

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile # this sets our serialize to point to our user profile model.
        # we wanna specify a list of fields in our model that we want to manage through our serialization.
        fields = ('id', 'email', 'name', 'password')
        # we wanna make exception too password field when creating new users, we don't wanna allow the users to retrieve the password hash because there's certain security risks 
        # Make password right only the way we do that is we use the extra keyword args for variable here. 
        extra_kwargs = {
            'password': {
                'write_only': True, # you can't able to retrieve objects.
                'style': {'input_type': 'password'}
            }
        }
        # This is going to be a dictionary and the keys of the dictionary are the fields that you wanna add to the custom configuration
        # Next thing we gonna do is overwrite the create function by default the model serializer allows you to create simple objects in the db. SO it uses the default create function of the object manager to create the object we want to override this functionality for this particular serialization so that it uses the create use of function instead of the create function. The reason we do this so that the password gets created as a hash and not the clear text password that it would do by default


    def create(self, validated_data):
        """Create a return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password'],
        )
        return user