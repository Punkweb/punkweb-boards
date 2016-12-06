from django.shortcuts import render
from rest_framework import viewsets
from .models import EmailUser
from .serializers import EmailUserSerializer

# Create your views here.

class EmailUserViewSet(viewsets.ModelViewSet):
    queryset = EmailUser.objects.all()
    serializer_class = EmailUserSerializer
