import uuid
from django.db import models
from django.contrib.auth.models import User


class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
     

    def __str__(self):
        return self.name
# Create your models here.
class Task(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    details = models.TextField()
    description = models.TextField()
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title