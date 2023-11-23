from rest_framework import serializers
from .models import MessageThread, Message

class MessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%d/%b/%y %H:%M:%S",read_only = True)
    sent_by = serializers.ReadOnlyField(source = 'sent_by.name')
    sent_by_id = serializers.ReadOnlyField(source = 'sent_by.id')
    class Meta:
        model = Message
        fields = "__all__"

class MessageThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many = True, read_only = True)
    first_user_id = serializers.ReadOnlyField(source = 'first_user.id')
    second_user_id = serializers.ReadOnlyField(source = 'second_user.id')
    first_user = serializers.ReadOnlyField(source = 'first_user.name')
    second_user = serializers.ReadOnlyField(source = 'second_user.name')

    class Meta:
        model = MessageThread
        fields = [
            'id','first_user_id','second_user_id','first_user',
            'second_user','messages','query'
        ]