from dolfinrest.models import DolfinImage, DolfinDate, DolfinDirname
from django.db.models import Q
from django.db.models import Count
from django.core.management.base import BaseCommand
import json
import sys

class Command(BaseCommand):
    help = "Customized load data for DB migration"

    def handle(self, **options):
        print(sys.path)