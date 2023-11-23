from django.urls import path
from .views import GetAllMessageThreadsAPIView, GetThreadAPIView

urlpatterns = [
    path("get-thread/<int:user_id>/<int:query_id>", GetThreadAPIView.as_view()),
    path("get-all-threads/", GetAllMessageThreadsAPIView.as_view()),
]