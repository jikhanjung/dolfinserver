from dolfinrest.models import DolfinDate, DolfinImage, DolfinBox
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from .models import UserActivity
from django.forms import inlineformset_factory
from dolfinrest.forms import DolfinBoxForm #AuthorForm, JournalForm, ReferenceForm, ReferenceAuthorForm, ScientificNameForm, LithoUnitForm, ChronoUnitForm, ScientificNameAuthorForm, ReferenceTaxonForm, ReferenceTaxonSpecimenForm, UserForm, NewUserForm
from django.shortcuts import render, get_object_or_404
from dolfinserver.settings import MEDIA_ROOT
from django.core.paginator import Paginator
from django.http import FileResponse
from PIL import Image
import io

LOGIN_URL = 'user_login'
ITEMS_PER_PAGE = 20

# Create your views here.
 
def get_user_obj( request ):
    user_obj = request.user
    if str(user_obj) == 'AnonymousUser':
        return None
    #print("user_obj:", user_obj)
    user_obj.groupname_list = []
    for g in request.user.groups.all():
        user_obj.groupname_list.append(g.name)

    if user_obj.username == 'invisible_admin':
        return user_obj
    # LOG user activity
    user_activity = UserActivity()
    user_activity.user = request.user
    user_activity.method = request.method
    user_activity.activity_url = request.path
    user_activity.save()

    return user_obj

def check_admin(user_obj):
    if 'Professors' in user_obj.groupname_list:
        #print(user_obj.username)
        return True
    else:
        return False

def dfw_date_list(request):
    user_obj = get_user_obj( request )
    selected_date = request.GET.get('selected_date','')
    date_list = DolfinDate.objects.all()
    if selected_date != '':
        date_list = date_list.filter(observation_date=selected_date)
    #date_list = date_list.order_by("observation_date")

    paginator = Paginator(date_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dolfinweb/dfw_date_list.html', {'date_list': date_list, 'page_obj': page_obj, 'user_obj': user_obj, 'selected_date':selected_date})

def dfw_image_list(request, obs_date):
    user_obj = get_user_obj( request )

    image_list = DolfinImage.objects.filter(exifdatetime__date=obs_date)
    paginator = Paginator(image_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    image_id_list = [ img.id for img in page_obj ]

    request.session['obs_date'] = obs_date
    request.session['page_number'] = page_number
    request.session['last_list'] = 'dfw_image_list'
    request.session['image_id_list'] = image_id_list
    print("page_number in image_list:", page_number)

    return render(request, 'dolfinweb/dfw_image_list.html', {'image_list': image_list, 'page_obj': page_obj, 'user_obj': user_obj, 'obs_date':obs_date })


def get_prev_next_image_and_page(a_image,a_image_id_list):
    next_image_set = DolfinImage.objects.filter(exifdatetime__gte=a_image.exifdatetime,filename__gt=a_image.filename).order_by("exifdatetime","filename")
    prev_image_set = DolfinImage.objects.filter(exifdatetime__lte=a_image.exifdatetime,filename__lt=a_image.filename).order_by("-exifdatetime","-filename")
    next_image = None
    prev_image = None
    if( len(next_image_set) >0):
        next_image = next_image_set[0]
        print(next_image.id,next_image.exifdatetime,next_image.filename)
    if( len(prev_image_set) >0):
        prev_image = prev_image_set[0]
        print(prev_image.id,prev_image.exifdatetime,prev_image.filename)

    page_number_diff = 0
    if a_image.id not in a_image_id_list:
        first_image_in_page = DolfinImage.objects.get(pk=a_image_id_list[0])
        last_image_in_page = DolfinImage.objects.get(pk=a_image_id_list[-1])
        if a_image.exifdatetime > last_image_in_page.exifdatetime or \
            ( a_image.exifdatetime == last_image_in_page.exifdatetime and a_image.filename > last_image_in_page.filename ):
            page_number_diff = 1
        elif a_image.exifdatetime < first_image_in_page.exifdatetime or \
             ( a_image.exifdatetime == first_image_in_page.exifdatetime and a_image.filename > first_image_in_page.filename ):
            page_number_diff = -1

    return prev_image,next_image,page_number_diff

def get_prev_next_finbox(a_finbox, a_finbox_id_list):
    next_finbox_set = DolfinBox.objects.filter(exifdatetime__gte=a_finbox.exifdatetime,id__gt=a_finbox.id).order_by("exifdatetime","id")
    prev_finbox_set = DolfinBox.objects.filter(exifdatetime__lte=a_finbox.exifdatetime,id__lt=a_finbox.id).order_by("-exifdatetime","-id")
    next_finbox = None
    prev_finbox = None
    if( len(next_finbox_set) >0):
        next_finbox = next_finbox_set[0]
        #print(next_image.id,next_image.exifdatetime,next_image.filename)
    if( len(prev_finbox_set) >0):
        prev_finbox = prev_finbox_set[0]
        #print(prev_image.id,prev_image.exifdatetime,prev_image.filename)

    page_number_diff = 0
    if a_finbox.id not in a_finbox_id_list:
        first_finbox_in_page = DolfinImage.objects.get(pk=a_finbox_id_list[0])
        last_finbox_in_page = DolfinImage.objects.get(pk=a_finbox_id_list[-1])
        if a_finbox.exifdatetime > last_finbox_in_page.exifdatetime or \
            ( a_finbox.exifdatetime == last_finbox_in_page.exifdatetime and a_finbox.id > last_finbox_in_page.id ):
            page_number_diff = 1
        elif a_finbox.exifdatetime < first_finbox_in_page.exifdatetime or \
             ( a_finbox.exifdatetime == first_finbox_in_page.exifdatetime and a_finbox.filename > first_finbox_in_page.filename ):
            page_number_diff = -1


    return prev_finbox, next_finbox, page_number_diff

def dfw_image_view(request, pk):
    user_obj = get_user_obj( request )

    image = DolfinImage.objects.get(pk=pk)
    
    last_list = request.session['last_list']
    page_number = int(request.session['page_number']) or 1
    obs_date = request.session['obs_date']
    print("page_number:",page_number)
    #if last_list == 'dfw_image_list':
    image_id_list = request.session['image_id_list']
    prev_image, next_image, page_number_diff = get_prev_next_image_and_page(image,image_id_list)
    #if page_number != request.session['page_number']:
    if page_number_diff != 0 :
        page_number += page_number_diff
        image_list = DolfinImage.objects.filter(exifdatetime__date=obs_date)
        paginator = Paginator(image_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
        page_obj = paginator.get_page(page_number)
        request.session['page_number'] = page_number
        request.session['image_id_list'] = [ img.id for img in page_obj ]
        
    context = {
        'image': image, 
        'user_obj': user_obj, 
        'last_list': last_list, 
        'page_number': page_number, 
        'obs_date': obs_date,
        'prev_image': prev_image,
        'next_image': next_image,
    }

    return render(request, 'dolfinweb/dfw_image_view.html', context)

def dfw_edit_finbox(request, pk, finid=None):
    user_obj = get_user_obj( request )
    #if( finid ):
    #    print("finid:",finid)

    image = get_object_or_404(DolfinImage,pk=pk)
    if request.method == 'POST':
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm)
        dolfinbox_formset = DolfinBoxFormSet(request.POST, instance=image)
        #print("post")
        if dolfinbox_formset.is_valid():
            #print("form valid")
            #print(dolfinbox_formset)
            boxset = dolfinbox_formset.save(commit=False)
            for box in boxset:
                box.exifdatetime = image.exifdatetime
                box.save()
            for delete_value in dolfinbox_formset.deleted_objects:
                delete_value.delete()
            image.update_thumbnail()
            image.save()

        else:
            print("box form invlid")
            print(dolfinbox_formset.errors)
        return HttpResponseRedirect(reverse('dfw_image_view',args=(pk,)))
    else:
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm,extra=0)
        dolfinbox_formset = DolfinBoxFormSet(instance=image)
         
    return render(request, 'dolfinweb/dfw_edit_finbox.html', {'image': image, 'user_obj': user_obj, 'dolfinbox_formset':dolfinbox_formset, 'finid':finid})

def dfw_fin_list(request, obs_date):
    user_obj = get_user_obj( request )

    fin_list = DolfinBox.objects.filter(exifdatetime__date=obs_date)
    paginator = Paginator(fin_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    for fin in page_obj:
        fin.get_coords()

    request.session['obs_date'] = obs_date
    request.session['page_number'] = page_number
    request.session['last_list'] = 'dfw_fin_list'
    #print("page_number in finbox_list:", page_number)

    #request.session['image_id_list'] = image_id_list
    context = {
        'fin_list': fin_list, 
        'page_obj': page_obj, 
        'user_obj': user_obj, 
        'obs_date':obs_date, 
    }

    return render(request, 'dolfinweb/dfw_fin_list.html', context)

def dfw_fin_image(request, pk):

    fin = DolfinBox.objects.get(pk=pk)
    image = fin.dolfin_image
    filepath = MEDIA_ROOT + str(image.imagefile)
    im = Image.open(filepath)
    [left,top,right,bottom] = [int(x) for x in fin.coords_str.split(",") ]
    im1 = im.crop((left, top, right, bottom))
    buf = io.BytesIO()
    im1.save(buf, format='JPEG')
    buf.seek(0)

    return FileResponse(buf)
    
