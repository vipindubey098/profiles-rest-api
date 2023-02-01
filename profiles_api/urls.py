from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset') 
# to register viewsets with our viewsets, we gonna access hello/viewsets, router will create all 4 urls for us, we don't need to specify, second arguments is the viewset we wish to register this url. Finally we need to specify a base name for our viewset. (hello-viewset)->This is gonna be used for retreving the url in our routers. Now add this in urlpatterns.

#registering our view sets
router.register('profile', views.UserProfileViewSet)

router.register('feed', views.UserProfileFeedViewSet)

urlpatterns= [
    path('hello-view/', views.HelloApiView.as_view()), 
    #as_view() - It is standard function that we call to convert our API view class to be rendered by urls.

    #adding in between this for login end point in django
    path('login/', views.UserLoginApiView.as_view()),
    # After running url in the browser go to 127.0.0.1:8000/api/login, now type any email/username and password in the browser then it will give us a token, which we can use in future reference

    path('', include(router.urls)),
    # As we register routes with our routers it generates a list of urls that are associated for our viewsets. It figures out the url that are required for all of the functions that we need to use our viewset and that it generates this url list which we can pass in using the path functions and include function. The reason we specify a blank string here is because we don't want to put a prefix to this URL. We just want all of the URL in the blank part and thats how you register view sets.
]