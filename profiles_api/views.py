from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# The status object from the rest framework is the of handle Http status codes that you can use when returning responses from your api. We gonna use this status codes in our post function handler
from profiles_api import serializers
# We are gonna tell our API view what data to expect when making post, put and patch requests

class HelloApiView(APIView):
    """Test API View"""
    
    serializer_class = serializers.HelloSerializer # This configure our api view to have serialized class that we have created, so this says whenever you're making or sending a post, put, or patch request expect and input with name and we're going to validate that input to a maximum length of 10 

    def get(self, request, format=None):
        """Returns a list of API View Features"""
        an_apiview = [
            'Uses Http methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional django view',
            'Gives you control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data) #self.serializer is a class function that comes with the API View that retrieves the configured serialized class for our view. SO it is standard way that you should retrieve the serialized class in a view.
        #validating serializer:
        if serializer.is_valid():
            name = serializer.validated_data.get('name') # fetching name field from serializer
            message = f'Hello {name}'
            return Response({'message': message})
        # If the input is not valid, then we will return http 400 bad request.
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # by default it returns http 200 response

    

    def put(self, request, pk=None):
        """Handling updating an object"""
        return Response({'method': 'PUT'})


    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        # patch will update only those which are provided to update
        return Response({'method': 'PATCH'})


    def delete(self, request, pk=None):
        """Delete an objects"""
        return Response({'method': 'DELETE'})