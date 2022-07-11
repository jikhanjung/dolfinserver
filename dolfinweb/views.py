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

def dfw_image_list(request, obs_date):
    user_obj = get_user_obj( request )

    image_list = DolfinImage.objects.filter(exifdatetime__date=obs_date)
    paginator = Paginator(image_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    request.session['obs_date'] = obs_date
    request.session['image_list_page'] = page_number

    return render(request, 'dolfinweb/dfw_image_list.html', {'image_list': image_list, 'page_obj': page_obj, 'user_obj': user_obj, 'obs_date':obs_date })

def dfw_date_list(request):
    user_obj = get_user_obj( request )
    selected_date = request.GET.get('selected_date','')
    date_list = DolfinDate.objects.all()
    if selected_date != '':
        date_list = date_list.filter(dolfin_date=selected_date)

    paginator = Paginator(date_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dolfinweb/dfw_date_list.html', {'date_list': date_list, 'page_obj': page_obj, 'user_obj': user_obj, 'selected_date':selected_date})

def dfw_image_view(request, pk):
    user_obj = get_user_obj( request )

    image = DolfinImage.objects.get(pk=pk)
    page_number = request.session['image_list_page']
    obs_date = request.session['obs_date']

    return render(request, 'dolfinweb/dfw_image_view.html', {'image': image, 'user_obj': user_obj, 'page_number':page_number, 'obs_date': obs_date})

def dfw_edit_finbox(request, pk, finid=None):
    user_obj = get_user_obj( request )
    if( finid ):
        print("finid:",finid)

    image = get_object_or_404(DolfinImage,pk=pk)
    if request.method == 'POST':
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm)
        dolfinbox_formset = DolfinBoxFormSet(request.POST, instance=image)
        print("post")
        if dolfinbox_formset.is_valid():
            print("form valid")
            print(dolfinbox_formset)
            boxset = dolfinbox_formset.save(commit=False)

            for box in boxset:
                box.exifdatetime = image.exifdatetime
                box.save()
            for delete_value in dolfinbox_formset.deleted_objects:
                delete_value.delete()                    

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
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    request.session['date'] = obs_date
    request.session['fin_list_page'] = page_number

    return render(request, 'dolfinweb/dfw_fin_list.html', {'fin_list': fin_list, 'page_obj': page_obj, 'user_obj': user_obj, 'date':obs_date })

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
    
