from django.shortcuts import render
from . models import Projects, Task, UserProfile
from . serializers import (
    ProjectsSerializer, TaskSerializer, RegisterSerializer, 
    UserSerializer, UserProfileSerializer
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Anyone can register
    serializer_class = RegisterSerializer


# Get Current User Info (with profile)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_current_user(request):
    """Get the currently authenticated user with profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Update User Profile
class UpdateProfileView(generics.RetrieveUpdateAPIView):
    """View and update the authenticated user's profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the profile of the logged-in user
        return self.request.user.profile


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