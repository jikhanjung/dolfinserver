from dolfinrest.models import DolfinImage, DolfinDate
from django.db.models import Q
from django.db.models import Count
from django.core.management.base import BaseCommand
from dolfinserver.settings import MEDIA_ROOT
import json
import os
from PIL import Image

class Command(BaseCommand):
    help = "Customized load data for DB migration"

    def handle(self, **options):
        print("generate thumbnail for DolfinImage")


        image_list = DolfinImage.objects.all()
        for image in image_list:
            #print(image.filename, image.imagefile)
            image_path = os.path.join( MEDIA_ROOT , str(image.imagefile ))
            #print(image.filename, image.imagefile, image_path)
            head, tail = os.path.split(image_path)
            new_head = os.path.join(head,'thumbnail')
            if not os.path.isdir(new_head):
                os.mkdir(new_head)
            thumbnail_path = os.path.join(new_head,tail)
            print(image.filename, image_path, thumbnail_path)
            if not os.path.isfile(thumbnail_path):
                img = Image.open(image_path)
                w, h = img.size
                new_w = 400
                new_h = int(h * ( 400 / w ))
                res_img = img.resize((new_w,new_h))
                res_img.save(thumbnail_path)
                #generate thumbnail




