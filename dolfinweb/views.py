from dolfinrest.models import DolfinDate, DolfinImage, DolfinBox
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from .models import UserActivity
from django.forms import inlineformset_factory
from dolfinrest.forms import DolfinBoxForm #AuthorForm, JournalForm, ReferenceForm, ReferenceAuthorForm, ScientificNameForm, LithoUnitForm, ChronoUnitForm, ScientificNameAuthorForm, ReferenceTaxonForm, ReferenceTaxonSpecimenForm, UserForm, NewUserForm
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator

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

    return render(request, 'dolfinweb/dfw_image_list.html', {'image_list': image_list, 'page_obj': page_obj, 'user_obj': user_obj, 'date':obs_date })

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

    return render(request, 'dolfinweb/dfw_image_view.html', {'image': image, 'user_obj': user_obj, })

def dfw_edit_finbox(request, pk):
    user_obj = get_user_obj( request )

    image = get_object_or_404(DolfinImage,pk=pk)
    if request.method == 'POST':
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm)
        dolfinbox_formset = DolfinBoxFormSet(request.POST, instance=image)
        if dolfinbox_formset.is_valid():
            dolfinbox_formset.save()
        else:
            print("box form invlid")
            print(dolfinbox_formset.errors)
        return HttpResponseRedirect(reverse('dfw_image_view',args=(pk,)))
    else:
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm,extra=5)
        dolfinbox_formset = DolfinBoxFormSet(instance=image)
         
    return render(request, 'dolfinweb/dfw_edit_finbox.html', {'image': image, 'user_obj': user_obj, 'dolfinbox_formset':dolfinbox_formset})