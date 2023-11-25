from django.urls import path
from .views import get_source_id, ChatBotAPIView, UploadChatBotFileAPIView

urlpatterns = [
    path("get-source-id/", get_source_id),
    path("chatbot/", ChatBotAPIView.as_view()),
    path("upload-pdf/", UploadChatBotFileAPIView.as_view())
]