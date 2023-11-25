from rest_framework import serializers
from .models import ChatBotFile

class ChatBotFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotFile
        fields = "__all__"