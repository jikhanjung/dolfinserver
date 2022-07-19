from django.contrib import admin
from .models import DolfinUser, DolfinDate, DolfinImage, DolfinDirname, DolfinBox
admin.site.register(DolfinUser)
admin.site.register(DolfinDate)
admin.site.register(DolfinImage)
admin.site.register(DolfinDirname)
admin.site.register(DolfinBox)
# Register your models here.
