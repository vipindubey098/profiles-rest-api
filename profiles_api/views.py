from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# The status object from the rest framework is the of handle Http status codes that you can use when returning responses from your api. We gonna use this status codes in our post function handler
from profiles_api import serializers
# We are gonna tell our API view what data to expect when making post, put and patch requests
from rest_framework import viewsets
from profiles_api import models
from rest_framework.authentication import TokenAuthentication 
# The token authentication is a type of authentication we use for users to authenticate themselves with our API it works by generating a random token string when the users logs in and then every request we make to that API that we need to authenticate we add this token string to the request and that's effectively a password to check that every request made is authenticated correctly 
from profiles_api import permissions

# Importing filter modules from rest_framework
from rest_framework import filters
# Out of the box the rest framework comes with some modules that we use to add filtering to a view.


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



class HelloViewSet(viewsets.ViewSet):
    """Test Api Viewsets"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message':'Hello!','a_viewset': a_viewset})


    def create(self, request):
        """Create a new hello message"""
        #Retrieving our serializers
        serializer = self.serializer_class(data=request.data)
        
        #validation
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}!'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle Removing an object"""
        return Response({'http_method': 'DELETE'})




class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() # fetching data
    #authentication 
    authentication_classes = (TokenAuthentication,) # Remember to add comma after token authentication so that this gets created as a tuple instead of just a single item
    # We can configure one or more type of authentication with a particular view set in the django rest framework. The way it works is you just add all the authentication classes to this authentication class variable.
    # Next we gonna add permissions classes so the authentication course is set how the user will authenticate that is the mechanism they will use and the permission classes say set how the user gets permissions to do certain things    
    permission_classes = (permissions.UpdateOwnProfile,)
    # adding filters
    filter_backends = (filters.SearchFilter,)
    # Below filter package we need to add one more class variable called search fields. This tells the filter backend which fields we're going to make searchable by this filter site.
    search_fields = ('name','email',)