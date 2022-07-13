from dolfinrest.models import DolfinImage, DolfinDate
from django.db.models import Q
from django.db.models import Count
from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):
    help = "Customized load data for DB migration"

    def handle(self, **options):
        print("DolfinDate update")


        image_list = DolfinImage.objects.all()
        for image in image_list:
            image.count_finboxes()
            image.save()

