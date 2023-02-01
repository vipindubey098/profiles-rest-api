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
# Adding obtain auth token
# This is a view that comes with Django Rest Framework, we can use to generate auth token
from rest_framework.authtoken.views import ObtainAuthToken
# Importing API Settings
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# As the name suggest this(IsAuthenticatedOrReadOnly) make sure a view site is read only if the user is not authenticated.

# Without authentication no one can we or write also
# We can remove IsAuthenticatedOrReadOnly or replace it with IsAuthenticated
from rest_framework.permissions import IsAuthenticated
# It blocks access to entire endpoint unless the user is authenticated.


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


# Creating a class called userloginapiview
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    # ObtainAuthToken is provided by django, is very handy and we can add directly to a urls.py, however it does it by default enable itself in browsable django admin side. SO we need to override this class, customise it.
    # we add a class varible called render_classes = we gonna import default renderer class from the api settings thats why we gonna need to import api settings on top of file
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # It addes renderer_classes to our obtain auth token view which will enable in the django admin 
    # We gonna add url to this view to enable it. Go to urls.py now


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading & updating profile feed items"""
    # We gonna use token authentocation to authenticate requests to out endpoint
    authentication_classes = (TokenAuthentication,)
    # We gonna set the serializer class to serialize that we created previously.
    serializer_class = serializers.ProfileFeedItemSerializer
    # So this sets these serialize a class on our view set to the profile feed items serialize
    # Next we gonna assign the query set that's going to be managed through our view set.
    queryset = models.ProfileFeedItem.objects.all()
    # SO we going to manage all our profile feed item objects from our model in our view set. It wil sets up basic model view set that allows us to create and manage feed item objects in db
    # However as we said we want to set this user_profile from serializers.py to read only because we are going to set it based on the authenticated user in order to do that we need to add a perform create function to our model view set.
    # We gonna add a new permission that comes with django rest framework import on top -> from rest_framework.permissions import IsAuthenticatedOrReadOnly 
    # Add a new class variable 
    permission_classes = (
        permissions.UpdateOwnStatus,
        # IsAuthenticatedOrReadOnly,
        IsAuthenticated, # we can limit the api to authenticated user only, now no one can see or write if we run with authentication
    )

    def perform_create(self, serializer):
        """Sets the profile to the logged in user"""
        # Perform_create is a handy feature of django rest framework that allows you to override the behavior or customize the behavior for creating objects through a model view sets. So when a request gets made to our view sets it gets passed in to our serialized class and validated an then serialzer dot save function is called by default
        # If we need to customize the logic for creating an object then we can do this using they perform create function.
        # So this perform_create function will get call every time you do http post tou our view sets
        serializer.save(user_profile=self.request.user)
        # Explain above line : So when a new object is created in django rest framework cores perform create and it passes in the serializer that we are using to create the object the serializer is a model serializer. user_profile coloumn value will be requested or login user in db
        # Lets head over to urls.py to lin up our new view sets to a url.

