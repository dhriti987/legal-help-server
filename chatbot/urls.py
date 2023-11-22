from django.urls import path
from .views import get_source_id

urlpatterns = [
    path("get-source-id/", get_source_id)
]