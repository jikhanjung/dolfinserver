from rest_framework import serializers
from .models import DolfinImage

class DolfinImageSerializer(serializers.ModelSerializer):
    imagefile = serializers.ImageField(use_url=True)
    class Meta:
        model = DolfinImage
        fields = [ 'ipaddress', 'user', 'filepath', 'filename', 'md5hash', 'exifdate', 'imagefile' ]
