from dolfinrest.models import DolfinImage, DolfinDate, DolfinBox
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
        print("load detected fin data for DolfinImage")

        DolfinBox.objects.all().delete()

        image_list = DolfinImage.objects.all().order_by('obsdate','dirname','exifdatetime','filename')
        prev_obsdate = ''
        findata_lines = []
        findata_hash = {}
        image_count = 0
        finbox_count = 0
        for image in image_list:
            if image.obsdate != prev_obsdate:
                findata_lines = []
                findata_hash = {}
                image_path = os.path.join( MEDIA_ROOT , str(image.imagefile ))
                head, tail = os.path.split(image_path)
                new_head = os.path.join(head,'labels')
                findata_path = os.path.join(new_head,'detected_fins.txt')
                with open(findata_path) as f:
                    findata_lines = f.readlines()
                for idx, line in enumerate(findata_lines):
                    #
                    line = line.strip()
                    #if idx < 10:
                    #    print(line) 
                    imagename, classno, x1,y1,x2,y2 = line.split(" ")
                    if imagename not in findata_hash.keys():
                        findata_hash[imagename] = []
                    findata_hash[imagename].append([x1,y1,x2,y2])
            if image.filename in findata_hash.keys():
                #print(image.filename, findata_hash[image.filename])
                for finbox_data in findata_hash[image.filename]:
                    finbox_count += 1
                    #print(finbox_data)
                    finbox = DolfinBox()
                    finbox.dolfin_image = image
                    finbox.exifdatetime = image.exifdatetime
                    finbox.created_by = 'yolov5'
                    finbox.modified_by = 'yolov5'
                    finbox.coords_str = ",".join(finbox_data)
                    finbox.save()
            image.update_thumbnail()
            image.count_finboxes()
            image.save()
            image_count += 1
            if image_count % 100 == 0:
                print(image_count,"images", finbox_count, "finboxes processed...")
            prev_obsdate = image.obsdate
