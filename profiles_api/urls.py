from django.urls import path


from profiles_api import views

urlpatterns= [
    path('hello-view/', views.HelloApiView.as_view()), #It is standard function that we call to convert our API view class to be rendered by urls.
]