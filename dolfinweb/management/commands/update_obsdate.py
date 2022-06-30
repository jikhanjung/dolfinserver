from dolfinrest.models import DolfinImage, DolfinDate
from django.db.models import Q
from django.db.models import Count
from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):
    help = "Customized load data for DB migration"

    def handle(self, **options):
        print("DolfinDate update")


        group_by_result = DolfinImage.objects.values('exifdatetime__date').annotate(count=Count('filename')).values('exifdatetime__date','count').order_by('exifdatetime__date')
        for date_count in group_by_result:
            print(date_count)
            obsdate, created = DolfinDate.objects.get_or_create(observation_date=date_count['exifdatetime__date'])
            print(obsdate)
            obsdate.image_count = date_count['count']
            obsdate.save()
            print(date_count)

