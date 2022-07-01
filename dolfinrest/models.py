from django.db import models
from django.contrib.auth.models import AbstractUser

class DolfinDate(models.Model):
    observation_date = models.DateField()
    image_count = models.IntegerField(default=0,blank=True,null=True)
    last_modified = models.DateTimeField(auto_now=True)

def upload_path(instance, filename): 
    # return f'posts/{instance.content}/{filename}'
    dolfin_date = instance.exifdatetime.date() #.strftime('%Y-%m-%d')

    print(dolfin_date)
    dolfin_date, created = DolfinDate.objects.get_or_create(observation_date=dolfin_date)
    dolfin_date.image_count += 1
    dolfin_date.save()
    return '{:4d}/{:02d}/{:02d}/{}'.format(instance.exifdatetime.year, instance.exifdatetime.month, instance.exifdatetime.day,filename)

# Create your models here.
class DolfinImage(models.Model):
    #ipaddress = models.CharField(max_length=100, blank=True, default='')  #request.META.get('HTTP_X_REAL_IP')
    #user = models.CharField(max_length=100, blank=True, default='')
    #filepath = models.CharField(max_length=200, blank=True, default='')
    filename = models.CharField(max_length=100, blank=True, default='') 
    md5hash = models.CharField(max_length=200, blank=True, default='')
    exifdatetime = models.DateTimeField(blank=True,null=True)
    #imagefile = models.ImageField(upload_to ='%Y/%m/%d/')
    imagefile = models.ImageField(upload_to=upload_path)

class DolfinUser(AbstractUser):
    firstname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'이름')
    lastname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'성')
    
    @property
    def korean_fullname(self):
        return self.lastname + self.firstname

    def __str__(self):
        return self.username
