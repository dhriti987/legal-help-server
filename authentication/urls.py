from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", CustomObtainAuthToken.as_view()),
    path("user/<int:pk>", GetUserDetailView.as_view())
]
