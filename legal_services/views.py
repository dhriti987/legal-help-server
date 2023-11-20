from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
