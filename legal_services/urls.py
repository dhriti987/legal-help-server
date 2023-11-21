from django.urls import path
from .views import (
    ExpertiseListCreateAPIView,
    ExpertListCreateAPIView,
    ExpertGetUpdateDestroyView,
    QueryListCreateAPIView,
    QueryGetUpdateDestroyView,
    QueryFileCreateAPIView,
    QueryFileGetDestroyView,
)

urlpatterns = [
    path("expertise-list/", ExpertiseListCreateAPIView.as_view()),
    path("experts/", ExpertListCreateAPIView.as_view()),
    path("experts/<int:pk>/", ExpertGetUpdateDestroyView.as_view()),
    path("query/", QueryListCreateAPIView.as_view()),
    path("query/<int:pk>", QueryGetUpdateDestroyView.as_view()),
    path("query-file/", QueryFileCreateAPIView.as_view()),
    path("query-file/<int:pk>", QueryFileGetDestroyView.as_view()),
]
