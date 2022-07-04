from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import DolfinImage
from .serializers import DolfinImageSerializer

# Create your views here.
from rest_framework import viewsets
#from serializers import PersonSerializer
#from .models import Person


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DolfinImage
from .serializers import DolfinImageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def dolfinimage_list(request):
    """
    List all code dolfinimages, or create a new dolfinimage.
    """
    if request.method == 'GET':
        dolfinimages = DolfinImage.objects.all()
        serializer = DolfinImageSerializer(dolfinimages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DolfinImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class DolfinImageViewSet(viewsets.ModelViewSet):
#    queryset = DolfinImage.objects.all()
#    serializer_class = DolfinImageSerializer

@csrf_exempt
def dolfinimage_list_old(request):
    """
    List all code dolfinimages, or create a new dolfinimage.
    """
    print("eeasdf")
    if request.method == 'GET':
        dolfinimages = DolfinImage.objects.all()
        serializer = DolfinImageSerializer(dolfinimages, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DolfinImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def dolfinimage_detail_old(request, pk):
    """
    Retrieve, update or delete a code dolfinimage.
    """
    try:
        dolfinimage = DolfinImage.objects.get(pk=pk)
    except DolfinImage.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DolfinImageSerializer(dolfinimage)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DolfinImageSerializer(dolfinimage, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        dolfinimage.delete()
        return HttpResponse(status=204)

@csrf_exempt
def dolfinimage_detail_md5hash_old(request, md5hash):
    """
    Retrieve, update or delete a dolfin image.
    """
    try:
        dolfinimage = DolfinImage.objects.get(md5hash=md5hash)
    except DolfinImage.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DolfinImageSerializer(dolfinimage)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DolfinImageSerializer(dolfinimage, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        dolfinimage.delete()
        return HttpResponse(status=204)

@api_view(['GET', 'PUT', 'DELETE'])
def dolfinimage_detail(request, pk):
    """
    Retrieve, update or delete a dolfin image.
    """
    try:
        dolfinimage = DolfinImage.objects.get(pk=pk)
    except DolfinImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DolfinImageSerializer(dolfinimage)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DolfinImageSerializer(dolfinimage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dolfinimage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def dolfinimage_detail_md5hash(request, md5hash,filename):
    """
    Retrieve, update or delete a dolfin image.
    """
    try:
        dolfinimage = DolfinImage.objects.filter(md5hash=md5hash).filter(filename=filename)
        if len( dolfinimage ) > 0:
            dolfinimage = dolfinimage[0]
            #print(dolfinimage)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except DolfinImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DolfinImageSerializer(dolfinimage)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DolfinImageSerializer(dolfinimage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dolfinimage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DolfinImageList(APIView):
    """
    List all dolfinimages, or create a new dolfinimage.
    """
    def get(self, request, format=None):
        dolfinimages = DolfinImage.objects.all()
        serializer = DolfinImageSerializer(dolfinimages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DolfinImageSerializer(data=request.data)
        #print(request.data)
        if serializer.is_valid():
            image_instance = serializer.save()
            image_instance.generate_thumbnail()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

class DolfinImageDetail(APIView):
    """
    Retrieve, update or delete a dolfinimage instance.
    """
    def get_object(self, pk):
        try:
            return DolfinImage.objects.get(pk=pk)
        except DolfinImage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dolfinimage = self.get_object(pk)
        serializer = DolfinImageSerializer(dolfinimage)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dolfinimage = self.get_object(pk)
        serializer = DolfinImageSerializer(dolfinimage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dolfinimage = self.get_object(pk)
        dolfinimage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)