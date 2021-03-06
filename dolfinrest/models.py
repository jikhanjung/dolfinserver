from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from dolfinserver.settings import MEDIA_ROOT
from PIL import Image, ImageDraw

class DolfinDate(models.Model):
    observation_date = models.DateField()
    image_count = models.IntegerField(default=0,blank=True,null=True)
    last_modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["observation_date"]
    @property
    def get_formatted_date(self):
        return self.observation_date.strftime("%Y-%m-%d")

class DolfinDirname(models.Model):
    observation_date = models.DateField()
    dirname = models.CharField(max_length=200, blank=True, default='')
    image_count = models.IntegerField(default=0,blank=True,null=True)
    last_modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["observation_date","dirname"]
                

def upload_path(instance, filename): 
    # return f'posts/{instance.content}/{filename}'
    l_date = instance.exifdatetime.date() #.strftime('%Y-%m-%d')
    dirname = instance.dirname

    #instance.obsdate = dolfin_date.strftime('%Y-%m-%d')
    #instance.obsdate = l_date

    #print(dolfin_date)
    dolfin_date, created = DolfinDate.objects.get_or_create(observation_date=l_date)
    dolfin_date.image_count += 1
    dolfin_date.save()
    dolfin_dir, created = DolfinDirname.objects.get_or_create(observation_date=l_date,dirname=dirname)
    dolfin_dir.image_count += 1
    dolfin_dir.save()
    
    return 'nas/{:4d}/{:02d}/{:02d}/{}'.format(instance.exifdatetime.year, instance.exifdatetime.month, instance.exifdatetime.day,filename)

# Create your models here.
class DolfinImage(models.Model):
    #ipaddress = models.CharField(max_length=100, blank=True, default='')  #request.META.get('HTTP_X_REAL_IP')
    #user = models.CharField(max_length=100, blank=True, default='')
    #filepath = models.CharField(max_length=200, blank=True, default='')
    filename = models.CharField(max_length=100, blank=True, default='') 
    md5hash = models.CharField(max_length=200, blank=True, default='')
    exifdatetime = models.DateTimeField(blank=True,null=True)
    obsdate = models.DateField(blank=True,null=True)
    #imagefile = models.ImageField(upload_to ='%Y/%m/%d/')
    imagefile = models.ImageField(upload_to=upload_path)
    dirname = models.CharField(max_length=200, blank=True, default='')
    finbox_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["exifdatetime","filename"]
        indexes = [
           models.Index(fields=['exifdatetime', 'filename',]),
        ]
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

    def update_thumbnail(self):
        #print("generate thumbnail")
        image_path = os.path.join( MEDIA_ROOT , str(self.imagefile ))
        #print(image.filename, image.imagefile, image_path)
        head, tail = os.path.split(image_path)
        new_head = os.path.join(head,'thumbnail')
        if not os.path.isdir(new_head):
            os.mkdir(new_head)
        thumbnail_path = os.path.join(new_head,tail)
        #print(self.filename, image_path, thumbnail_path)
        img = Image.open(image_path)            
        for finbox in self.finboxes.all():
            coords = finbox.get_coords()
            #print(coords)
            img_ctx = ImageDraw.Draw(img)
            img_ctx.rectangle([(coords[0],coords[1]),(coords[2],coords[3])], outline ="red", width=20)
        #img.save("d:/temp/test.jpg")
        w, h = img.size
        new_w = 400
        new_h = int(h * ( 400 / w ))
        res_img = img.resize((new_w,new_h))
        res_img.save(thumbnail_path)
        #generate thumbnail        

    def count_finboxes(self):
        self.finbox_count = self.finboxes.all().count()


class DolfinUser(AbstractUser):
    firstname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'??????')
    lastname = models.CharField( max_length=50, blank=True, null=True,verbose_name=u'???')
    
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
    created_by = models.CharField(max_length=50,blank=True,null=True,default='')
    modified_on = models.DateTimeField(blank=True,null=True,auto_now=True)
    modified_by = models.CharField(max_length=50,blank=True,null=True,default='')
    
    class Meta:
        ordering = ["exifdatetime","id"]
    
    def get_coords(self):
        coords = [ int(x) for x in self.coords_str.split(",") ]
        self.width = coords[2] - coords[0]
        self.height = coords[3] - coords[1]
        self.whratio = float(self.width) / float(self.height)
        return coords
