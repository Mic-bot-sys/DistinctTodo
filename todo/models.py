from django.db import models
from django.conf import settings
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False)
    content = models.TextField()
    isCompleted = models.BooleanField(default=False)
    
    # ForeignKey Fields
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE, related_name='todoCreatedBy')
    
     # Other Fields
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateCompleted = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    dateDeleted = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDeleted = models.BooleanField(default=False)

    
    class Meta:
        verbose_name_plural = 'List'
    
    
    def __str__(self):
        return f"{self.title}"
    
    
    


