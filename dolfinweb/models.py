from django.db import models
from dolfinrest.models import DolfinUser

# Create your models here.
class UserActivity(models.Model):
    user = models.ForeignKey(DolfinUser, on_delete=models.CASCADE,related_name='fsis_activities')
    activity_url = models.CharField(max_length=200,blank=True,null=True)
    method = models.CharField(max_length=20,blank=True,null=True)
    activity_datetime = models.DateTimeField(blank=True,null=True,auto_now_add=True) 
