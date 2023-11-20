from django.urls import path
from .views import (
    ExpertiseListCreateAPIView
)

urlpatterns = [
    path("expertise-list/", ExpertiseListCreateAPIView.as_view())
]
