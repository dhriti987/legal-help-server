from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .permissions import *

# Create your views here.
class ExpertiseListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Expertise.objects.all()
    serializer_class = ExpertiseSerializer

class ExpertListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class ExpertGetUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class QueryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QuerySerializer
    queryset = Query.objects.all()

    def get_queryset(self):
        if self.request.user.user_type == "COMMON":
            return self.queryset.filter(user = self.request.user)
        elif self.request.user.expert == None:
            return ValidationError(detail="User Don't Have Expert Details")
        return self.queryset.filter(catagory = self.request.user.expert.expertise, is_resolved=False)
    

class QueryGetUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ObjectGetUpdateDeletePermission]
    serializer_class = QuerySerializer
    queryset = Query.objects.all()

class QueryFileCreateAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QueryFileSerializer
    queryset = QueryFile.objects.all()

class QueryFileGetDestroyView(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ObjectGetUpdateDeletePermission]
    serializer_class = QueryFileSerializer
    queryset = QueryFile.objects.all()