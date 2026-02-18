from . import views
from django.urls import path, include
from rest_framework import routers
from . views import TaskViewSet, get_current_user, UpdateProfileView

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'projects', views.ProjectsViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', get_current_user, name='current_user'),          # Get current user info
    path('profile/', UpdateProfileView.as_view(), name='profile'), # View/Update profile
]