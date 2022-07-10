from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from dolfinserver.settings import MEDIA_ROOT
from PIL import Image

class DolfinDate(models.Model):
    observation_date = models.DateField()
    image_count = models.IntegerField(default=0,blank=True,null=True)
    last_modified = models.DateTimeField(auto_now=True)

def upload_path(instance, filename): 
    # return f'posts/{instance.content}/{filename}'
    dolfin_date = instance.exifdatetime.date() #.strftime('%Y-%m-%d')

    #print(dolfin_date)
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
    dirname = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ["exifdatetime"]

    @property
    def get_thumbnail_url(self):
        image_url = self.imagefile.url
        #print(image.filename, image.imagefile, image_path)
        head, tail = os.path.split(image_url)
        new_head = os.path.join(head,'thumbnail')
        #if not os.path.isdir(new_head):
        #    os.mkdir(new_head)
        thumbnail_path = os.path.join(new_head,tail)
        return thumbnail_path

    def generate_thumbnail(self):
        #print("generate thumbnail")
        image_path = os.path.join( MEDIA_ROOT , str(self.imagefile ))
        #print(image.filename, image.imagefile, image_path)
        head, tail = os.path.split(image_path)
        new_head = os.path.join(head,'thumbnail')
        if not os.path.isdir(new_head):
            os.mkdir(new_head)
        thumbnail_path = os.path.join(new_head,tail)
        #print(self.filename, image_path, thumbnail_path)
        if not os.path.isfile(thumbnail_path):
            img = Image.open(image_path)
            w, h = img.size
            new_w = 400
            new_h = int(h * ( 400 / w ))
            res_img = img.resize((new_w,new_h))
            res_img.save(thumbnail_path)
            #generate thumbnail        

class DolfinUser(AbstractUser):
    firstname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'이름')
    lastname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'성')
    
    @property
    def korean_fullname(self):
        return self.lastname + self.firstname

    def __str__(self):
        return self.username

class DolfinBox(models.Model):
#post_id = models.ForeignKey("Post", related_name="post", on_delete=models.CASCADE, db_column="post_id")    
    dolfin_image = models.ForeignKey("DolfinImage",related_name="finboxes",on_delete=models.CASCADE)
    coords_str = models.CharField(max_length=100,blank=True,null=True,default='')
    boxname = models.CharField(max_length=100,blank=True,null=True,default='')
    boxcolor = models.CharField(max_length=20,blank=True,null=True,default='')
    exifdatetime = models.DateTimeField(blank=True,null=True)
    created_on = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    created_by = models.CharField(max_length=20,blank=True,null=True,default='')
    modified_on = models.DateTimeField(blank=True,null=True,auto_now=True)
    modified_by = models.CharField(max_length=20,blank=True,null=True,default='')
    
