from . import views
from django.urls import path, include
from rest_framework import routers
from . views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'projects', views.ProjectsViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]