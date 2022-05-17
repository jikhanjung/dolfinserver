from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class DolfinImage(models.Model):
    ipaddress = models.CharField(max_length=100, blank=True, default='')  #request.META.get('HTTP_X_REAL_IP')
    user = models.CharField(max_length=100, blank=True, default='')
    filepath = models.CharField(max_length=200, blank=True, default='')
    filename = models.CharField(max_length=100, blank=True, default='')
    md5hash = models.CharField(max_length=200, blank=True, default='')
    imagefile = models.ImageField(upload_to ='%Y/%m/%d/')

class DolfinUser(AbstractUser):
    firstname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'이름')
    lastname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'성')
    
    @property
    def korean_fullname(self):
        return self.lastname + self.firstname

    def __str__(self):
        return self.username
