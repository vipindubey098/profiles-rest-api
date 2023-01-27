from rest_framework import serializers


#We will create a new class called hello serializers
class HelloSerializer(serializers.Serializer):
    """Serialzers a new field for testing our APIView"""
    # we're gonna create a simple serializer name input, an then we gonna us it to test the post functionality of out APIView, These function is similar to django forms
    # Define the serializer and then you specify the fields that you wanna accept in serializer the input
    # Serializers also take care of validation rules, if you want to accept a certain field of a certain type this will make sure that the content pass the API is of the correct type that you want to require the field
    name = serializers.CharField(max_length=10)

    # Adding post functionality to our APIView
     