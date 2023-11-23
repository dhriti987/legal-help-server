from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from chat.models import MessageThread, Query
from .serializers import MessageThreadSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

class GetThreadAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, query_id):
        first_user = request.user
        second_user = get_user_model().objects.get(id = user_id)
        query = Query.objects.get(id = query_id)
        if first_user == second_user:
            raise ValidationError("Cannot make thread With Self")
        if first_user.id > second_user.id:
            first_user, second_user = second_user, first_user
        thread, _ = MessageThread.objects.get_or_create(first_user=first_user, second_user=second_user, query=query)
        
        return Response(MessageThreadSerializer(thread).data)
    
class GetAllMessageThreadsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageThreadSerializer

    def get_queryset(self):
        return MessageThread.objects.by_user(user = self.request.user)