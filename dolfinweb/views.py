from dolfinrest.models import DolfinDate, DolfinImage, DolfinBox, DolfinUser
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from .models import UserActivity
from django.forms import inlineformset_factory
from dolfinrest.forms import DolfinBoxForm  #AuthorForm, JournalForm, ReferenceForm, ReferenceAuthorForm, ScientificNameForm, LithoUnitForm, ChronoUnitForm, ScientificNameAuthorForm, ReferenceTaxonForm, ReferenceTaxonSpecimenForm, UserForm, NewUserForm
from dolfinweb.forms import UserForm, NewUserForm
from django.shortcuts import render, get_object_or_404
from dolfinserver.settings import MEDIA_ROOT
from django.core.paginator import Paginator
from django.http import FileResponse
from PIL import Image
import io
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime


LOGIN_URL = 'dfw_user_login'
ITEMS_PER_PAGE = 20

# Create your views here.
 
def get_user_obj( request ):
    user_obj = request.user
    #print(user_obj)
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
    if 'Administrators' in user_obj.groupname_list:
        #print(user_obj.username)
        return True
    else:
        return False

def dfw_date_list(request):
    user_obj = get_user_obj( request )
    print(user_obj)
    selected_date = request.GET.get('selected_date','')
    date_list = DolfinDate.objects.all()
    if selected_date != '':
        date_list = date_list.filter(observation_date=selected_date)
    #date_list = date_list.order_by("observation_date")

    paginator = Paginator(date_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dolfinweb/dfw_date_list.html', {'date_list': date_list, 'page_obj': page_obj, 'user_obj': user_obj, 'selected_date':selected_date})

@never_cache
def dfw_image_list(request, obs_date):
    print("image list 1", datetime.now())

    user_obj = get_user_obj( request )
    get_obs_date = request.POST.get('obs_date','')
    if get_obs_date != '':
        obs_date = get_obs_date

    filter1 = request.POST.get('filter1','all')
    print("image list 2", datetime.now())
    
    image_list = DolfinImage.objects.filter(exifdatetime__date=obs_date)

    print("image list 3", datetime.now())
    if filter1 == 'no_fins':
        #print("filter1 on: no fins")
        image_list = image_list.filter(finbox_count=0)
    #print(image_list)
    print("image list 4", datetime.now())

    paginator = Paginator(image_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    print("image list 4.1", datetime.now())
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    print("image list 4.2", datetime.now())
    image_id_list = [ img.id for img in page_obj ]
    print("image list 5", datetime.now())

    obs_date_list = DolfinDate.objects.all()

    request.session['obs_date'] = obs_date
    request.session['page_number'] = page_number
    request.session['last_list'] = 'dfw_image_list'
    request.session['image_id_list'] = image_id_list
    print("page_number in image_list:", page_number)
    print("image list 6", datetime.now())

    context = {
        'image_list': image_list, 
        'page_obj': page_obj, 
        'user_obj': user_obj, 
        'obs_date':obs_date, 
        'obs_date_list': obs_date_list,
        'filter1': filter1,
    }

    return render(request, 'dolfinweb/dfw_image_list.html', context)


def _get_prev_next_image_and_page(a_image,a_image_id_list):
    next_image_set = DolfinImage.objects.filter(exifdatetime__gte=a_image.exifdatetime,filename__gt=a_image.filename).order_by("exifdatetime","filename")
    prev_image_set = DolfinImage.objects.filter(exifdatetime__lte=a_image.exifdatetime,filename__lt=a_image.filename).order_by("-exifdatetime","-filename")
    next_image = None
    prev_image = None
    if( len(next_image_set) >0):
        next_image = next_image_set[0]
        #print(next_image.id,next_image.exifdatetime,next_image.filename)
    if( len(prev_image_set) >0):
        prev_image = prev_image_set[0]
        #print(prev_image.id,prev_image.exifdatetime,prev_image.filename)

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
    pn = request.session.get('page_number') or 1
    page_number = int(pn)
    obs_date = request.session['obs_date']
    #print("page_number:",page_number)
    #if last_list == 'dfw_image_list':
    image_id_list = request.session['image_id_list']
    prev_image, next_image, page_number_diff = _get_prev_next_image_and_page(image,image_id_list)
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

@login_required(login_url=LOGIN_URL)
def dfw_edit_finbox(request, pk, finid=None):
    user_obj = get_user_obj( request )
    #if( finid ):
    #    print("finid:",finid)

    image = get_object_or_404(DolfinImage,pk=pk)

    last_list = request.session['last_list']
    pn = request.session.get('page_number') or 1
    page_number =  int(pn)
    obs_date = request.session['obs_date']
    #print("page_number:",page_number)
    #if last_list == 'dfw_image_list':
    image_id_list = request.session['image_id_list']
    prev_image, next_image, page_number_diff = _get_prev_next_image_and_page(image,image_id_list)
    #if page_number != request.session['page_number']:
    if page_number_diff != 0 :
        page_number += page_number_diff
        image_list = DolfinImage.objects.filter(exifdatetime__date=obs_date)
        paginator = Paginator(image_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
        page_obj = paginator.get_page(page_number)
        request.session['page_number'] = page_number
        request.session['image_id_list'] = [ img.id for img in page_obj ]

    if request.method == 'POST':
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm)
        dolfinbox_formset = DolfinBoxFormSet(request.POST, instance=image)
        print("post")
        if dolfinbox_formset.is_valid():
            print("form valid")
            #print(dolfinbox_formset)
            boxset = dolfinbox_formset.save(commit=False)
            for box in boxset:
                box.exifdatetime = image.exifdatetime
                print("box id:",box.id)
                if box.id is None:
                    box.created_by = user_obj.username
                box.modified_by = user_obj.username
                box.save()
            for delete_value in dolfinbox_formset.deleted_objects:
                delete_value.delete()
            image.update_thumbnail()
            image.count_finboxes()
            image.save()

        else:
            print("box form invlid")
            print(dolfinbox_formset.errors)
        return HttpResponseRedirect(reverse('dfw_edit_finbox',args=(pk,)))
    else:
        DolfinBoxFormSet = inlineformset_factory(DolfinImage,DolfinBox,form=DolfinBoxForm,extra=0)
        dolfinbox_formset = DolfinBoxFormSet(instance=image)

    context = {
        'image': image, 
        'user_obj': user_obj, 
        'last_list': last_list, 
        'page_number': page_number, 
        'obs_date': obs_date,
        'prev_image': prev_image,
        'next_image': next_image,
        'dolfinbox_formset':dolfinbox_formset, 
        'finid': finid,
    }

    return render(request, 'dolfinweb/dfw_edit_finbox.html', context )

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

@never_cache
def dfw_fin_image(request, img_id, fin_id_or_coords_str):

    coords = [ int(x) for x in fin_id_or_coords_str.split(",") ]
    fin_id = None
    image = DolfinImage.objects.get(pk=img_id)
    if len(coords) != 4:
        fin = DolfinBox.objects.get(pk=fin_id_or_coords_str)
        coords = [int(x) for x in fin.coords_str.split(",") ]

    print(coords)
    filepath = MEDIA_ROOT + str(image.imagefile)
    im = Image.open(filepath)
    
    im1 = im.crop(coords)
    max_wh = 150
    if im1.width > im1.height:
        new_width = max_wh
        new_height = int(max_wh * im1.height / im1.width)
    else:
        new_height = max_wh
        new_width = int(max_wh * im1.width / im1.height)
    im1 = im1.resize((new_width,new_height))
    buf = io.BytesIO()
    im1.save(buf, format='JPEG')
    buf.seek(0)

    return FileResponse(buf)

def dfw_user_login(request):
    next = '/dolfinweb/dashboard'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.GET.get('next'):
            next = request.GET.get('next')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'dolfinweb/dfw_user_login_form.html')
        
        user_obj = get_user_obj( request )
    else:
        return render(request, 'dolfinweb/dfw_user_login_form.html')

    return redirect(next)

@login_required(login_url=LOGIN_URL)
def dfw_user_logout(request):
    user_obj = get_user_obj( request )
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=LOGIN_URL)
def dfw_user_change_password(request):
    user_obj = get_user_obj( request )

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/dolfinweb/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dolfinweb/dfw_user_change_password.html', {
        'user_obj':user_obj,'form': form
    })    

@login_required(login_url=LOGIN_URL)
def dfw_user_info(request):
    user_obj = get_user_obj( request )

    #print(user_obj.username)
    return render(request, 'dolfinweb/dfw_user_info.html', {'user_obj': user_obj} )

@login_required(login_url=LOGIN_URL)
def dfw_user_edit(request):
    user_obj = get_user_obj( request )

    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dolfinweb/dfw_user_info')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm(instance=user_obj)

    return render(request, 'dolfinweb/dfw_user_form.html', {'form': form,'user_obj':user_obj})

def dfw_user_register(request):
    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dolfinweb/dfw_user_info')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewUserForm()

    return render(request, 'dolfinweb/dfw_user_register_form.html', {'form': form })


# User management by admin
@login_required(login_url=LOGIN_URL)
def dfw_user_list_admin(request):
    user_obj = get_user_obj( request )
    if not check_admin( user_obj ):
        print("check admin fail")
        return HttpResponseRedirect('/dolfinweb')

    user_list = DolfinUser.objects.all().order_by('username')
    for user in user_list:
        user.groupname_list = []
        for g in user.groups.all():
            user.groupname_list.append(g.name)
    print(user_list)

    #print(user_obj.username)
    return render(request, 'dolfinweb/dfw_user_list_admin.html', {'user_obj': user_obj, 'user_list': user_list} )    

@login_required(login_url=LOGIN_URL)
def dfw_user_detail_admin(request,pk):
    user_obj = get_user_obj( request )
    check_admin( user_obj )

    user = get_object_or_404(DolfinUser, pk=pk)
    #groups = user.groups.all()
    #print(groups)

    #print(user_obj.username)
    return render(request, 'dolfinweb/dfw_user_detail_admin.html', {'user_obj': user_obj,'user': user} )

@login_required(login_url=LOGIN_URL)
def dfw_user_activity_list_admin(request,pk):
    user_obj = get_user_obj( request )
    if not check_admin( user_obj ):
        #print("check admin fail")
        return HttpResponseRedirect('/dolfinweb')
    
    activity_list = UserActivity.objects.filter(user=pk).order_by('-activity_datetime')

    #print(activity_list)
    #print(user_obj.username)
    #return render(request, 'kprdb/user_list_admin.html', {'user_obj': user_obj, 'activity_list': activity_list} )

    paginator = Paginator(activity_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dolfinweb/dfw_activity_list_admin.html', {'activity_list': activity_list, 'page_obj': page_obj, 'user_obj': user_obj})

@login_required(login_url=LOGIN_URL)
def dfw_user_add_admin(request):
    user_obj = get_user_obj( request )
    check_admin( user_obj )

    if request.method == 'POST':
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dfw_user_list_admin'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewUserForm()

    return render(request, 'dolfinweb/dfw_user_register_form.html', {'form': form, 'user_obj': user_obj })

@login_required(login_url=LOGIN_URL)
def dfw_user_edit_admin(request,pk):
    user_obj = get_user_obj( request )
    check_admin( user_obj )

    user = get_object_or_404(DolfinUser, pk=pk)
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dfw_user_detail_admin',args=(user.id,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm(instance=user)

    return render(request, 'dolfinweb/dfw_user_form_admin.html', {'form': form,'user_obj':user_obj,'user':user})

@login_required(login_url=LOGIN_URL)
def dfw_user_change_password_admin(request,pk):
    user_obj = get_user_obj( request )
    check_admin( user_obj )
    print(user_obj.group)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/dolfinweb/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dolfinweb/dfw_user_change_password.html', {
        'user_obj':user_obj,'form': form
    })    

@login_required(login_url=LOGIN_URL)
def dfw_user_delete_admin(request,pk):
    user_obj = get_user_obj( request )
    check_admin( user_obj )

    user = get_object_or_404(DolfinUser, pk=pk)
    user.delete()
    return HttpResponseRedirect(reverse('dfw_user_list_admin'))    

@login_required(login_url=LOGIN_URL)
def dfw_all_activity_list_admin(request):
    user_obj = get_user_obj( request )
    if not check_admin( user_obj ):
        #print("check admin fail")
        return HttpResponseRedirect('/dolfinweb')
    
    activity_list = UserActivity.objects.all().order_by('-activity_datetime')

    #print(activity_list)
    #print(user_obj.username)
    #return render(request, 'kprdb/user_list_admin.html', {'user_obj': user_obj, 'activity_list': activity_list} )

    paginator = Paginator(activity_list, ITEMS_PER_PAGE) # Show ITEMS_PER_PAGE contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dolfinweb/dfw_activity_list_admin.html', {'activity_list': activity_list, 'page_obj': page_obj, 'user_obj': user_obj})

@login_required(login_url=LOGIN_URL)
def dfw_history_overview(request):
    return    
