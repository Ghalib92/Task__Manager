from django.shortcuts import render
from . models import Projects, Task
from . serializers import ProjectsSerializer, TaskSerializer, RegisterSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Anyone can register
    serializer_class = RegisterSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'details', 'description', 'priority']
    ordering_fields = ['start_date', 'due_date', 'priority']

    def get_queryset(self):
        # Users can only see their own tasks
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user when creating a task
        serializer.save(user=self.request.user)


class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        # Users can only see their own projects
        return Projects.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user when creating a project
        serializer.save(user=self.request.user)