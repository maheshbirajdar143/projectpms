from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, Count, Sum
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
import matplotlib.pyplot as plt
from datetime import date
from io import BytesIO
from .models import *
from .forms import *
import pandas as pd
import base64
import json, time
from datetime import datetime
	
############################################################################################################################################

def home_view(request):                                                                                          # Initial Home Page
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'user/index.html')

############################################################################################################################################

def studentclick_view(request):                                                                                  # Artist Click
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'user/studentclick.html')

############################################################################################################################################

def adminclick_view(request):                                                                                    # Admin Click
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'user/adminclick.html')

############################################################################################################################################

def adminsignup_view(request):                                                                                   # Admin Register
    form1 = AdminSigupForm()
    form2 = AdminExtraForm()
    context = {'form1':form1,'form2':form2}
    if request.method=='POST':
        form1 = AdminSigupForm(request.POST)
        form2 = AdminExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2          = form2.save(commit=False)
            f2.user     = user 
            user2       = f2.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            messages.success(request,f'Your account has created successfully')
            return HttpResponseRedirect('adminlogin')
        else:
            messages.error(request,f'Something went wrong')
    else:
        context['form1'] = form1  
        context['form2'] = form2
    return render(request,'user/adminsignup.html', context)

############################################################################################################################################

def studentsignup_view(request):                                                                                  # Artist Register
    form1 = StudentSignupForm()
    form2 = StudentExtraForm()
    context = {'form1':form1,'form2':form2}
    if request.method=='POST':
        form1 = StudentSignupForm(request.POST)
        form2 = StudentExtraForm(request.POST)
        
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2          = form2.save(commit=False)
            f2.user     = user 
            user2       = f2.save()

            my_student_group = Group.objects.get_or_create(name='ARTIST')
            my_student_group[0].user_set.add(user)

            return HttpResponseRedirect('studentlogin')
        
        else:
            context['form1'] = form1  
            context['form2'] = form2
    return render(request,'user/studentsignup.html',context)
 
############################################################################################################################################

def is_admin(user):                                                                                               # Admin Group
    return user.groups.filter(name='ADMIN').exists()

############################################################################################################################################

def afterlogin_view(request):                                                                                     # After login
    if is_admin(request.user):
        return render(request,'user/adminafterlogin.html')
    else:
        return render(request,'user/studentafterlogin.html')

############################################################################################################################################

class CustomLoginView(LoginView):                                                                                 # Artist Login
    template_name = 'user/studentlogin.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        UserActivity.objects.create(user=self.request.user, login_time=timezone.now())
        return response

############################################################################################################################################

class CustomLogoutView(LogoutView):                                                                               # Artist Logout
    next_page = 'h'  

    def dispatch(self, request, *args, **kwargs):
        UserActivity.objects.filter(user=request.user, logout_time__isnull=True).update(logout_time=timezone.now())
        return super().dispatch(request, *args, **kwargs)

############################################################################################################################################

'''
def logged_in_users(request):                                                                                      # Online Artist
    artist_group = Group.objects.get(name='ARTIST')
    artist_available = UserActivity.objects.exists()
    logged_in_users = UserActivity.objects.filter(user__groups=artist_group, logout_time__isnull=True)
    logged_in_users_count = logged_in_users.count()
    
    context = {'logged_in_users': logged_in_users, 
               'logged_in_users_count': logged_in_users_count,
               'artist_available' : artist_available
               }
    return render(request, 'user/logged_in_users.html', context)
'''


def logged_in_users(request):                                                                                      # Online Artist
    try:
        artist_group = Group.objects.get(name='ARTIST')
    except ObjectDoesNotExist:
        artist_group = None 
    
    if artist_group:
        logged_in_users = UserActivity.objects.filter(user__groups=artist_group, logout_time__isnull=True)
        logged_in_users_count = logged_in_users.count()
    else:
        logged_in_users = []
        logged_in_users_count = 0
    
    artist_available = UserActivity.objects.exists()

    context = {
        'logged_in_users': logged_in_users,
        'logged_in_users_count': logged_in_users_count,
        'artist_available': artist_available,
    }
    return render(request, 'user/logged_in_users.html', context)

###############################################################################################################################################

def change_password(request):                                                                                    # Password Change
    user = request.user
    admin_group = is_admin(user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully updated.')

            if is_admin(request.user):
                return redirect('adminlogin')
            else:
                return redirect('studentlogin')

    form = PasswordChangeForm(user=request.user)
    context = {'form': form, 'admin_group': admin_group}
    return render(request, 'user/passchange.html', context)

############################################################################################################################################

def UpdateUserProfile(request):                                                                                   # Change Email
    user = request.user
    admin_group = is_admin(user)

    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,"Your email has been successfully updated.")
            if admin_group:
                return redirect('alladmin1')
            else:
                return redirect('h')
    
    u_form = UserUpdateForm(instance=request.user)
    context = {'u_form': u_form, 'admin_group': admin_group}
    return render(request,'user/userupdate.html', context)
            
###############################################################################################################################################

@login_required(login_url='adminlogin')
def search_shot2_admin(request):                                                                                 # Search All Data Admin
    query = request.GET.get('q')

    if query:
        query = query.strip()
        results = Shot2.objects.filter(
            Q(project_name__istartswith     =query) |
            Q(shot_name__istartswith        =query) |
            Q(work_description__istartswith =query) |
            Q(dependency__istartswith       =query) |
            Q(work_status__istartswith      =query) |
            Q(final_status__istartswith     =query) |
            Q(internal_status__istartswith  =query) |
            Q(remark__istartswith           =query) |
            Q(client_status__istartswith    =query) 
        )
    else:
        results = []

    context = {'results': results}
    return render(request, 'user/search_all_admin.html', context)

#################################################################################################################################################

@login_required(login_url='studentlogin')
def search_shot2_artist(request):                                                                                    # Search All Data Artist
    query = request.GET.get('p')

    if query:
        query = query.strip()
        results = Shot2.objects.filter(
            Q(project_name__istartswith     =query) |
            Q(shot_name__istartswith        =query) |
            Q(work_description__istartswith =query) |
            Q(dependency__istartswith       =query) |
            Q(work_status__istartswith      =query) |
            Q(final_status__istartswith     =query) |
            Q(internal_status__istartswith  =query) |
            Q(remark__istartswith           =query) |
            Q(client_status__istartswith    =query) )
    else:
        results = []

    context = {'results': results}
    return render(request, 'user/search_all_artist.html', context)

##################################################################################################################################################
############################################################    A) ADMIN PORTAL      #############################################################
##################################################################################################################################################

def allartist_view(request):                                                                                                          # All Artist
    user = request.user
    is_admin_group = is_admin(user)

    artists = StudentExtra.objects.all().order_by('user__first_name', 'user__last_name')
    context = {'artists':artists, 'is_admin_group':is_admin_group}
    return render(request,'user/allartist.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def alladmin_view(request):                                                                                                           # All Admin
    # admin_group = Group.objects.get(name='ADMIN')
    # user_data = admin_group.user_set.all()
    # admins = [{'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'username': user.username } for user in user_data]
    # context = {'admins':admins}
    admins = AdminExtra.objects.all().order_by('user__first_name', 'user__last_name')
    context = {'admins':admins}
    return render(request,'user/alladmin.html', context)

##################################################################################################################################################

@login_required(login_url='adminlogin')                                                                                        # Edit/Update Artist 
@user_passes_test(is_admin)
def editartist_view(request, id):
    object = get_object_or_404(StudentExtra, id=id)
    if request.method == "POST":
        form = StudentExtraForm(request.POST, instance=object)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Artist details updated successfully!')
            return redirect('allartist1')
    else:
        form = StudentExtraForm(instance=object)
    context = {'form':form,'object': object,}
    return render(request,'user/editartist.html',context)
    
##################################################################################################################################################
#                                                                  1) PRODUCTION  
##################################################################################################################################################

@login_required(login_url='adminlogin')                                                                            # Add New Project
@user_passes_test(is_admin)
def addproject_view(request):
    form = ShotForm()
    if request.method == 'POST':
        form = ShotForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data.get('project_name')
            shot_names = form.cleaned_data.get('shot_name')
            shot_names = shot_names.split('\n')  

            existing_shot_names  = set(Shot2.objects.filter(project_name=project_name).values_list('shot_name', flat=True))
            new_shot_names       = []
            duplicate_shot_names = []
            
            for shot_name in shot_names:
                shot_name = shot_name.strip() 

                if shot_name and shot_name not in existing_shot_names and shot_name not in new_shot_names:
                    new_shot_names.append(shot_name)

                elif shot_name in existing_shot_names or shot_name in new_shot_names:
                    duplicate_shot_names.append(shot_name)
            
            if duplicate_shot_names:
                messages.error(request, f'Remove duplicate shot names: {", ".join(duplicate_shot_names)}')
            else:
                for shot_name in new_shot_names:
                    shot = Shot2.objects.create(
                        dependency       = form.cleaned_data.get('dependency'),
                        project_name     = project_name,
                        shot_name        = shot_name,
                        work_description = form.cleaned_data.get('work_description'),
                        date_started     = form.cleaned_data.get('date_started'),
                        eta              = form.cleaned_data.get('eta'),
                        work_status      = form.cleaned_data.get('work_status'),
                        final_status     = form.cleaned_data.get('final_status'),
                        remark           = form.cleaned_data.get('remark'),
                        client_status    = form.cleaned_data.get('client_status'),)
                messages.success(request, f'Project {project_name} added successfully!')
                return redirect('allproject')  
    context = {'form': form}
    return render(request, 'user/addproject.html', context)

#################################################################################################################################################

@login_required(login_url='adminlogin')                                                                              # Delete Individual Project 
def delete_project(request, project_name):
    Shot2.objects.filter(project_name=project_name).delete()
    IssuedShot.objects.filter(project_name=project_name).delete()
    messages.success(request, f'Project ({project_name}) removed successfully.')
    return redirect('allproject')

##################################################################################################################################################

@login_required(login_url='adminlogin')                                                                              # All Project List
def allproject_view(request):
    projects = Shot2.objects.values('project_name').annotate(num_shots=Count('project_name'))
    context = {'projects': projects}
    return render(request, 'user/allproject.html', context)

####################################################################################################################################################

@login_required(login_url='adminlogin')                                                                               # All shot by selected project
def project_shots_view(request, project_name): 
    if request.method == 'POST':   
        for shot in Shot2.objects.filter(project_name=project_name):
            if shot.added_column:
                for column_name, _ in shot.added_column.items():
                    updated_value = request.POST.get(f'column_value_{shot.id}_{column_name}')
                    if updated_value is not None:
                        shot.added_column[column_name] = updated_value
                        shot.save()
                        messages.success(request, f'New value saved for shot ({shot.shot_name})')

        # for shot in Shot2.objects.filter(project_name=project_name):
        #     column_name = 'comp_status' 
        #     updated_value = request.POST.get(f'column_value_{shot.id}_{column_name}')
        #     if updated_value is not None:
        #         shot.comp_status = updated_value
        #         shot.save()
        #         messages.success(request, f'New value saved for shot ({shot.shot_name}) inside column ({column_name})')

        for shot in Shot2.objects.filter(project_name=project_name):
            for column_name in ['shot_version', 'comp_status','shot_name','dependency','work_description','eta','remark','client_status']:
                updated_value = request.POST.get(f'column_value_{shot.id}_{column_name}')
                if updated_value is not None:
                    column_mapping = {
                        'shot_name': 'shot_name',
                        'shot_version': 'shot_version',
                        'dependency': 'dependency',
                        'work_description': 'work_description',
                        'eta': 'eta',
                        'remark': 'remark',
                        'client_status': 'client_status',
                        'comp_status': 'comp_status',}
                    
                    previous_value = getattr(shot, column_mapping[column_name])
                    if updated_value != previous_value:
                        setattr(shot, column_mapping[column_name], updated_value)
                        shot.save()

                        ShotHistory.objects.create(
                            shot=shot,
                            field_name=column_mapping[column_name],
                            previous_value=previous_value,
                            updated_value=updated_value,
                            updated_by=request.user,)
                        messages.success(request, f'New value saved for shot ({shot.shot_name})')

        column_name = request.POST.get('new_column_name')
        remove_column_name = request.POST.get('remove_column')

        if column_name:
            for shot in Shot2.objects.filter(project_name=project_name):
                if shot.added_column is None:
                    shot.added_column = {}
                shot.added_column[column_name] = None
                shot.save()
            messages.success(request, f'Column ({column_name}) added successfully!')
            return redirect('pshots', project_name=project_name)

        elif remove_column_name:
            for shot in Shot2.objects.filter(project_name=project_name):
                if shot.added_column and remove_column_name in shot.added_column:
                    del shot.added_column[remove_column_name]
                    shot.save()
            messages.success(request, f'Column ({remove_column_name}) removed successfully!')
            return redirect('pshots', project_name=project_name)
        
    shots = Shot2.objects.filter(project_name=project_name).order_by('shot_name')
    project_added_date = shots.first().date_started
    project_TGT_Date = shots.first().eta

    items_per_page = 30
    paginator = Paginator(shots, items_per_page)
    page = request.GET.get('page')

    try:
        shots = paginator.page(page)
    except PageNotAnInteger:
        shots = paginator.page(1)
    except EmptyPage:
        shots = paginator.page(paginator.num_pages)

    all_column_names = set()
    for shot in shots:
        if shot.added_column:
            all_column_names.update(shot.added_column.keys())

    for shot in shots:
        if shot.added_column is None:
            shot.added_column = {}
        for column_name in all_column_names:
            if column_name not in shot.added_column:
                shot.added_column[column_name] = None
            shot.save()

    context = {'project_name': project_name, 
               'shots': shots, 
               'project_added_date': project_added_date,
               'project_TGT_Date': project_TGT_Date}
    return render(request, 'user/pshots.html', context)


####################################################################################################################################################

@login_required(login_url='adminlogin')                                                                            # Add Shot inside current Project
@user_passes_test(is_admin)
def addshot_project(request, project_name):
    form = ShotForm()
    if request.method == 'POST':
        form = ShotForm(request.POST)
        if form.is_valid():
            shot_names = form.cleaned_data.get('shot_name')
            #shot_names = shot_names.split('\n') 
            shot_names = shot_names.splitlines()

            existing_shot_names = set(Shot2.objects.filter(project_name=project_name).values_list('shot_name', flat=True)) 
            new_shot_names = []

            for shot_name in shot_names:
                shot_name = shot_name.strip()
                if shot_name in existing_shot_names:
                    messages.error(request, f'Shot name ({shot_name}) already exists in project {project_name}.')
                else:
                    new_shot_names.append(shot_name)

            if new_shot_names:
                for shot_name in new_shot_names:
                    shot = Shot2.objects.create(
                        dependency       = form.cleaned_data.get('dependency'),
                        project_name     = project_name,
                        shot_name        = shot_name,
                        work_description = form.cleaned_data.get('work_description'),
                        date_started     = form.cleaned_data.get('date_started'),
                        eta              = form.cleaned_data.get('eta'), )
                    
                messages.success(request,f'Shot ({shot_name}) added successfully.')
                return redirect('pshots', project_name=project_name)
    
    context = {'project_name': project_name, 'form': form}
    return render(request, 'user/addshot_project.html', context)

####################################################################################################################################################

@login_required(login_url='adminlogin')                                                                              
@user_passes_test(is_admin)  
def shot_history_view(request, shot_id):                                                                               # Edit Shot  saved all changes view
    shot = get_object_or_404(Shot2, id=shot_id)
    history = ShotHistory.objects.filter(shot=shot).order_by('-updated_at')
    context = {'shot': shot, 'history': history}
    return render(request, 'user/update.html', context)



@login_required(login_url='adminlogin')                                                                                # Edit Shot  saved all changes
@user_passes_test(is_admin) 
def editshot_view(request, id):
    object = get_object_or_404(Shot2, id=id)
    if request.method == "POST":
        form = EditShotForm(request.POST, instance=object)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            for field_name, field in form.fields.items():
                cleaned_value = form.cleaned_data.get(field_name)
                initial_value = form.initial.get(field_name)

                if cleaned_value != initial_value:
                    previous_value = getattr(object, field_name)
                    ShotHistory.objects.create(
                        shot          =object,
                        field_name    =field_name,
                        previous_value=initial_value,
                        updated_value =cleaned_value,
                        updated_by    =request.user)
            messages.success(request, 'Shot updated successfully.')
            return redirect('pshots', project_name=data.project_name)
    else:
        form = EditShotForm(instance=object, initial={'dependency': object.dependency.split(',')})
    context = {'form': form, 'object': object}
    return render(request, 'user/editshot.html', context)




@login_required(login_url='adminlogin')                                                                                # Edit Shot1  saved all changes
@user_passes_test(is_admin) 
def editshot_view1(request, id):
    object = get_object_or_404(Shot2, id=id)
    if request.method == "POST":
        form = EditShotForm1(request.POST, instance=object)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            for field_name, field in form.fields.items():
                cleaned_value = form.cleaned_data.get(field_name)
                initial_value = form.initial.get(field_name)

                if cleaned_value != initial_value:
                    previous_value = getattr(object, field_name)
                    ShotHistory.objects.create(
                        shot           =object,
                        field_name     =field_name,
                        previous_value =initial_value,
                        updated_value  =cleaned_value,
                        updated_by     =request.user)
            messages.success(request, 'Shot updated successfully.')
            return redirect('pshots', project_name=data.project_name)
    else:
        form = EditShotForm1(instance=object, initial={'dependency': object.dependency.split(',')})
    context = {'form': form, 'object': object}
    return render(request, 'user/editshot1.html', context)

#############################################################################################################################################

@login_required(login_url='adminlogin')                                                                                 # Delete Individual Shot
@user_passes_test(is_admin)
def deleteshot_view(request, pk):
    shot_obj = get_object_or_404(Shot2, pk=pk)
    project_name = shot_obj.project_name
    shot_obj.delete()
    IssuedShot.objects.filter(project_name=project_name, shot_name=shot_obj.shot_name).delete()
    messages.success(request, 'Shot removed successfully!')
    return redirect('pshots', project_name=project_name)

#####################################################################################################################################################

def searchprojectshot_view(request):                                                                                   # Search Shot inside Project
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            shots = Shot2.objects.filter(
                Q(shot_name__icontains = query) |
                Q(work_status__icontains = query) |
                Q(final_status__icontains = query) )
            return render(request, 'user/search1.html', {'shots': shots})
    return render(request, 'user/search1.html')

###############################################################################################################################################

@login_required(login_url='adminlogin')                                                                                # Edit multiple Shot using \n (new line)
@user_passes_test(is_admin)
def update_work_status1(request, project_name):
    if request.method == 'POST':
        shot_names = request.POST.get('shot_names', '').split('\n')
        internal_status = request.POST.get('internal_status', '')
        shot_names = [name.strip() for name in shot_names if name.strip()]

        for shot_name in shot_names:
            shot = Shot2.objects.get(shot_name=shot_name)
            previous_internal_status = shot.internal_status
            ShotHistory.objects.create(
                shot=shot,
                field_name='internal_status',
                previous_value=previous_internal_status,
                updated_value=internal_status,
                updated_by=request.user)

        Shot2.objects.filter(shot_name__in=shot_names).update(internal_status=internal_status)
        messages.success(request, f'Internal status of shots ({", ".join(shot_names)}) updated successfully.')
    return redirect('pshots', project_name=project_name)

###############################################################################################################################################

@login_required(login_url='adminlogin')                                                                                # Edit multiple dependency
@user_passes_test(is_admin) 
def update_dependency1(request):
    if request.method == 'POST':
        shot_names = request.POST.get('shot_names', '').split(',')
        dependencies = request.POST.getlist('dependencies[]')  
        for shot_name in shot_names:
            Shot2.objects.filter(shot_name=shot_name).update(dependency=','.join(dependencies))
        messages.success(request, 'Dependency updated successfully!')
    return redirect('allproject')


################################################################################################################################################
#                                                                   2) TASK    
################################################################################################################################################

@login_required(login_url='adminlogin')                                                                   # Import Excel Data (File name --> Master.xls)
@user_passes_test(is_admin)
def import_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('file')
        if not excel_file:
            return render(request, 'user/importdata.html', {'message': 'No file selected.'})
                                            
        file_extension = excel_file.name.split('.')[-1].lower()
        
        if file_extension == 'xlsx':
            engine = 'openpyxl'
        elif file_extension == 'xls':
            engine = 'xlrd'
        else:
            return render(request, 'user/importdata.html', {'message': 'Invalid file format.'})

        try:
            df = pd.read_excel(excel_file, engine=engine)
        except Exception as e:
            return render(request, 'user/importdata.html', {'message': f"Error reading the Excel file: {e}"})

        expected_columns = ['Project Name', 'Shot Name', 'Date Created', 'Scope of Work', 'TGT Date', 'Dependency', 'Assign', 'Internal Status']
        missing_columns = [col for col in expected_columns if col not in df.columns]

        if missing_columns:
            return render(request, 'user/importdata.html', {'message': f"Columns are missing : {', '.join(missing_columns)}"})

        #df = pd.read_excel(excel_file, engine=engine)
        df.fillna('N/A', inplace=True) 
        imported_rows = 0
        error_rows = 0

        for index, row in df.iterrows():
            project_name = row['Project Name']
            shot_name    = row['Shot Name']

            existing_shot1 = Shot2.objects.filter(project_name=project_name, shot_name=shot_name).first()
            if existing_shot1:
                existing_shot1.date_started     = row['Date Created']
                existing_shot1.work_description = row['Scope of Work']
                existing_shot1.eta              = row['TGT Date']
                existing_shot1.save()

            existing_shot = Shot2.objects.filter(project_name=project_name, shot_name=shot_name).exists()
            if not existing_shot:
                date_started = row['Date Created']
                eta = row['TGT Date']
                if date_started < eta:
                    obj = Shot2.objects.create(
                        project_name     = project_name,
                        shot_name        = shot_name,
                        work_description = row['Scope of Work'],
                        date_started     = date_started,
                        eta              = eta,
                        dependency       = row['Dependency'],
                        work_status      = row['Assign'],
                        internal_status  = row['Internal Status'],)
                    obj.save()
                    imported_rows += 1
                else:
                    error_rows += 1

        time.sleep(3)
        
        if imported_rows > 0:
            message = f"New {imported_rows} shots added successfully."   
        else:
            message = "No New Data Found."

        if error_rows > 0:
            message += f" {error_rows} rows skipped due to invalid dates."

        return render(request, 'user/importdata.html', {'message': message, 'preview': df.to_html(classes='table table-bordered table-striped', header='true')})
    else:
        return render(request, 'user/importdata.html')

################################################################################################################################################

# @login_required(login_url='adminlogin')                                                                                 # All Projects Shot
# def allshot_view(request): 
#     shots = Shot2.objects.all().order_by('project_name')
#     context = {'shots': shots}
#     return render(request, 'user/allshot.html', context)




@login_required(login_url='adminlogin')                                                                                 # All Projects Shot
def allshot_view(request):
    shots = Shot2.objects.all().order_by('project_name')
    items_per_page = 30
    paginator = Paginator(shots, items_per_page)
    page = request.GET.get('page')

    try:
        shots = paginator.page(page)
    except PageNotAnInteger:
        shots = paginator.page(1)
    except EmptyPage:
        shots = paginator.page(paginator.num_pages)

    context = {'shots': shots}
    return render(request, 'user/allshot.html', context)





@login_required(login_url='adminlogin')                                                                              # View assigned department & status received 
def shot_department_view(request, id):
    shot = Shot2.objects.get(id=id)
    dep_notes = ShotDepNote.objects.filter(shot=shot)
    rec_notes = ShotDepNote.objects.filter(shot=shot)

    context = {
        'shot': shot,
        'dep_notes': dep_notes,
        'rec_notes' : rec_notes,}
    return render(request, 'user/shotdep.html', context)

################################################################################################################################################

@login_required(login_url='adminlogin')
def reviewed_shot(request, shot_id):
    try:
        shot = Shot2.objects.get(pk=shot_id)
        name = request.user.username

        if not name:
            return HttpResponseBadRequest('Name is required.')
        
        if name != request.user.username:
            raise HttpResponseBadRequest('Enter the correct username.')

        #shot.internal_status = f'REVIEWED (by {request.user.username})'
        #shot.internal_status = f'REVIEWED'
        shot.internal_status = f'Approved By Lead'
        version = shot.shot_version
        review = Review(shot=shot, reviewed_by=request.user, version=version)
        review.save()
        shot.save()
        messages.success(request, f'Shot (Version-{version}) Approved by {request.user.first_name} {request.user.last_name}.')

    except Shot2.DoesNotExist:
        messages.error(request, 'Shot does not exist')

    return redirect('allshot')

#################################################################################################################################################

def searchshot_view(request):                                                                                          # Search All Projects Shot
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            shots = Shot2.objects.filter(
                Q(project_name__istartswith=query) |
                Q(shot_name__istartswith=query) |
                Q(work_status__istartswith=query) )
            return render(request, 'user/search.html', {'shots': shots})
    return render(request, 'user/search.html') 
    
###################################################################################################################################################

def validate_shot_dependencies(shot, department):
    if not shot.dependency:
        return "Before assigning, set the dependencies for the given shot_name."
    if department not in shot.dependency:
        return f"The '{department}' department  does not exist in the dependency of the given shot and project."
    return None


def get_artists_by_department(request):
    department     = request.GET.get('department')
    artists        = StudentExtra.objects.filter(department=department).order_by('user__username')
    artist_choices = [(artist.id, artist.get_name) for artist in artists]
    return JsonResponse({'artists': artist_choices})


'''
@login_required(login_url='adminlogin')                                                                                      # Assign Shot to artist
@user_passes_test(is_admin)
def issueshot_view(request):
    form = IssuedShotForm()
    context = {'form': form}

    if request.method == 'POST':
        form = IssuedShotForm(request.POST, request.FILES)
        if form.is_valid():
            department   = form.cleaned_data['department1']
            artist       = form.cleaned_data['artist1']
            shot_name    = form.cleaned_data['shotname1']
            project_name = form.cleaned_data['projectname1']
            shot_version = form.cleaned_data['shotversion1']
            kbk_image    = form.cleaned_data['kbk_image1']

            try:
                shot = Shot2.objects.get(project_name=project_name, shot_name=shot_name)
            except Shot2.DoesNotExist:
                messages.error(request, 'The selected shot does not exist.')
            else:
                validation_error = validate_shot_dependencies(shot, department)
                if validation_error:
                    messages.error(request, validation_error)
                elif artist.department != department:
                    messages.error(request, 'Artist does not belong to the selected department.')
                else:     
                    IssuedShot.objects.create(
                        artist           = artist,
                        department       = department,
                        shot_name        = shot_name,
                        shot_version     = request.POST.get('shotversion1'),
                        work_description = request.POST.get('workdescription1'),
                        project_name     = project_name,
                        issuedate        = request.POST.get('issdate1'),
                        eta              = request.POST.get('eta1'),
                        note             = request.POST.get('note1'),
                        kbk_image        = kbk_image,
                        work_status      = 'Assigned',)
                    
                    messages.success(request, f'Shot ({shot_name}) assigned successfully.')
                    return redirect('viewissuedshot')
    else:
        shot_name        = request.GET.get('shot_name')
        project_name     = request.GET.get('project_name')
        work_description = request.GET.get('work_description')

        if shot_name and project_name:
            form.initial['shotname1']        = shot_name
            form.initial['projectname1']     = project_name
            form.initial['workdescription1'] = work_description

    context['form'] = form
    return render(request, 'user/issueshot.html', context)
'''


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issueshot_view(request):
    form = IssuedShotForm()
    context = {'form': form}

    if request.method == 'POST':
        form = IssuedShotForm(request.POST, request.FILES)
        if form.is_valid():
            department = form.cleaned_data['department1']
            artist = form.cleaned_data['artist1']
            shot_name = form.cleaned_data['shotname1']
            project_name = form.cleaned_data['projectname1']
            shot_version = form.cleaned_data['shotversion1']
            kbk_image = form.cleaned_data['kbk_image1']

            try:
                shot = Shot2.objects.get(project_name=project_name, shot_name=shot_name)
            except Shot2.DoesNotExist:
                messages.error(request, 'The selected shot does not exist.')
            else:
                validation_error = validate_shot_dependencies(shot, department)
                if validation_error:
                    messages.error(request, validation_error)
                elif artist.department != department:
                    messages.error(request, 'Artist does not belong to the selected department.')
                else:
                    existing_shots = IssuedShot.objects.filter(
                        project_name=project_name,
                        shot_name=shot_name,
                        department=department,)

                    if existing_shots.exists():
                        return render(
                            request,
                            'user/confdelete.html',
                            {
                                'existing_shots': existing_shots,
                                'new_shot': {
                                    'artist': artist,
                                    'department': department,
                                    'shot_name': shot_name,
                                    'shot_version': shot_version,
                                    'work_description': request.POST.get('workdescription1'),
                                    'project_name': project_name,
                                    'issuedate': request.POST.get('issdate1'),
                                    'eta': request.POST.get('eta1'),
                                    'note': request.POST.get('note1'),
                                    'kbk_image': kbk_image,
                                    'work_status': 'Assigned',
                                },
                            },)

                    IssuedShot.objects.create(
                        artist           =artist,
                        department       =department,
                        shot_name        =shot_name,
                        shot_version     =request.POST.get('shotversion1'),
                        work_description =request.POST.get('workdescription1'),
                        project_name     =project_name,
                        issuedate        =request.POST.get('issdate1'),
                        eta              =request.POST.get('eta1'),
                        note             =request.POST.get('note1'),
                        kbk_image        =kbk_image,
                        work_status      ='Assigned',)
                    messages.success(request, f'Shot ({shot_name}) assigned successfully.')
                    return redirect('viewissuedshot')
    else:
        shot_name        = request.GET.get('shot_name')
        project_name     = request.GET.get('project_name')
        work_description = request.GET.get('work_description')
        shot_version     = request.GET.get('shot_version')

        if shot_name and project_name:
            form.initial['shotname1']        = shot_name
            form.initial['projectname1']     = project_name
            form.initial['workdescription1'] = work_description
            form.initial['shotversion1']     = shot_version

    context['form'] = form
    return render(request, 'user/issueshot.html', context)

#######################################################################################################################################

def confirm_replace_shot(request):                                                                  # Re-Assign (Kick-internal) Shot to artist
    if request.method == 'POST':
        replace_choice = request.POST.get('replace')
        data_dict = request.POST.dict()

        if 'csrfmiddlewaretoken' in data_dict:
            del data_dict['csrfmiddlewaretoken']
        if 'replace' in data_dict:
            del data_dict['replace']

        if replace_choice == 'yes':
            IssuedShot.objects.filter(
                project_name=request.POST.get('project_name'),
                shot_name=request.POST.get('shot_name'),
                department=request.POST.get('department'),
            ).delete()

            IssuedShot.objects.create(**data_dict)
            messages.success(request, 'Shot replaced successfully.')
            
        else:
            IssuedShot.objects.create(**data_dict)
            messages.success(request, 'Shot assigned successfully.')
            
        return redirect('viewissuedshot')
    return redirect('viewissuedshot')

###################################################################################################################################################

@login_required(login_url='adminlogin')                                                                                      # Re-Assign (Kbk-TL) Shot to artist
@user_passes_test(is_admin)
def re_issueshot_view(request):
    form = IssuedShotForm()
    context = {'form': form}

    if request.method == 'POST':
        form = IssuedShotForm(request.POST, request.FILES)
        if form.is_valid():
            department   = form.cleaned_data['department1']
            artist       = form.cleaned_data['artist1']
            shot_name    = form.cleaned_data['shotname1']
            project_name = form.cleaned_data['projectname1']
            kbk_image    = form.cleaned_data['kbk_image1']

            try:
                shot = Shot2.objects.get(project_name=project_name, shot_name=shot_name)
            except Shot2.DoesNotExist:
                messages.error(request, 'The selected shot does not exist.')
            else:
                validation_error = validate_shot_dependencies(shot, department)
                if validation_error:
                    messages.error(request, validation_error)
                elif artist.department != department:
                    messages.error(request, 'Artist does not belong to the selected department.')
                else:
                    IssuedShot.objects.create(
                        artist           = artist,
                        department       = department,
                        shot_name        = shot_name,
                        shot_version     = request.POST.get('shotversion1'),
                        work_description = request.POST.get('workdescription1'),
                        project_name     = project_name,
                        issuedate        = request.POST.get('issdate1'),
                        eta              = request.POST.get('eta1'),
                        note             = request.POST.get('note1'),
                        kbk_image        = kbk_image,
                        work_status      = 'Kbk By Lead',)
                    
                    messages.success(request, f'Shot ({shot_name}) Kbk By Lead successfully.')
                    return redirect('viewissuedshot')
    else:
        shot_name        = request.GET.get('shot_name')
        project_name     = request.GET.get('project_name')
        work_description = request.GET.get('work_description')
        shot_version     = request.GET.get('shot_version')

        if shot_name and project_name:
            form.initial['shotname1']        = shot_name
            form.initial['projectname1']     = project_name
            form.initial['workdescription1'] = work_description
            form.initial['shotversion1']     = shot_version

    context['form'] = form
    return render(request,'user/reissueshot.html',context)

############################################################################################################################################

@login_required(login_url='adminlogin')                                                                                      # Re-Assign(Kick-back sup) Shot to artist
@user_passes_test(is_admin)
def re_issueshot_sup_view(request):
    form = IssuedShotForm()
    context = {'form': form}

    if request.method == 'POST':
        form = IssuedShotForm(request.POST, request.FILES)
        if form.is_valid():
            department   = form.cleaned_data['department1']
            artist       = form.cleaned_data['artist1']
            shot_name    = form.cleaned_data['shotname1']
            project_name = form.cleaned_data['projectname1']
            kbk_image    = form.cleaned_data['kbk_image1']

            try:
                shot = Shot2.objects.get(project_name=project_name, shot_name=shot_name)
            except Shot2.DoesNotExist:
                messages.error(request, 'The selected shot does not exist.')
            else:
                validation_error = validate_shot_dependencies(shot, department)
                if validation_error:
                    messages.error(request, validation_error)
                elif artist.department != department:
                    messages.error(request, 'Artist does not belong to the selected department.')
                else:
                    IssuedShot.objects.create(
                        artist           = artist,
                        department       = department,
                        shot_name        = shot_name,
                        shot_version     = request.POST.get('shotversion1'),
                        work_description = request.POST.get('workdescription1'),
                        project_name     = project_name,
                        issuedate        = request.POST.get('issdate1'),
                        eta              = request.POST.get('eta1'),
                        note             = request.POST.get('note1'),
                        kbk_image        = kbk_image,
                        work_status      = 'Kbk-Supervisor',)
                    
                    messages.success(request, f'Shot ({shot_name}) Kbk-Supervisor successfully.')
                    return redirect('viewissuedshot')
    else:
        shot_name        = request.GET.get('shot_name')
        project_name     = request.GET.get('project_name')
        work_description = request.GET.get('work_description')
        shot_version     = request.GET.get('shot_version')

        if shot_name and project_name:
            form.initial['shotname1']        = shot_name
            form.initial['projectname1']     = project_name
            form.initial['workdescription1'] = work_description
            form.initial['shotversion1']     = shot_version
            
    context['form'] = form
    return render(request,'user/reissueshotsup.html',context)


###################################################################################################################################################
#                                                                   3)  ARTIST    
###################################################################################################################################################

@login_required(login_url='adminlogin')                                                                                         # View Issued Shot
@user_passes_test(is_admin)
def viewissuedshot_view(request):
    issuedshots = IssuedShot.objects.all().order_by("shot_name")
    paginator = Paginator(issuedshots, 30)
    page = request.GET.get('page')
    issuedshots = paginator.get_page(page)

    def is_all_done(shot_name):
        return IssuedShot.objects.filter(shot_name=shot_name).exclude(work_status='READY FOR REVIEW').count() == 0
    
    li = []
    today = date.today()

    for issuedshot in issuedshots:
        if not hasattr(issuedshot, 'work_status') or issuedshot.work_status is None:
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(work_status='YTS')

        elif is_all_done(issuedshot.shot_name):
            department_to_highlight = issuedshot.department
            shot = Shot2.objects.get(shot_name=issuedshot.shot_name)
            # shot.dependency = shot.dependency.replace(department_to_highlight, f'<span class="highlight1">{department_to_highlight}</span>')
            shot.save()
            
        elif issuedshot.work_status == 'WIP':
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(internal_status='WIP')

        elif issuedshot.work_status == 'HOLD':
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(internal_status='HOLD')

        elif issuedshot.work_status == 'DONE':
            issuedshot.work_status = 'READY FOR REVIEW'
            department_to_highlight = issuedshot.department
            shot = Shot2.objects.get(shot_name=issuedshot.shot_name)
            # shot.dependency = shot.dependency.replace(department_to_highlight, f'<span class="highlight1">{department_to_highlight}</span>')
            #shot.save()
            depnote_instance, created = ShotDepNote.objects.get_or_create(shot=shot)
            recdepnotes = depnote_instance.recdepnotes or []
            if department_to_highlight not in recdepnotes:
                recdepnotes.append(department_to_highlight)
                depnote_instance.recdepnotes = recdepnotes
                depnote_instance.save()
            issuedshot.save()
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(internal_status='READY FOR REVIEW')

        elif issuedshot.work_status == 'READY FOR REVIEW':
            department_to_highlight = issuedshot.department
            shot = Shot2.objects.get(shot_name=issuedshot.shot_name)
            # shot.dependency = shot.dependency.replace(department_to_highlight, f'<span class="highlight1">{department_to_highlight}</span>')
            shot.save()
    
        elif issuedshot.work_status == 'Kbk By Lead':
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(internal_status='Kbk By Lead')
            department_to_highlight = issuedshot.department
            shot = Shot2.objects.get(shot_name=issuedshot.shot_name)
            # shot.dependency = shot.dependency.replace(department_to_highlight, f'<span class="highlight">{department_to_highlight}</span>')
            shot.save()

        elif issuedshot.work_status == 'Kbk-Supervisor':
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(internal_status='Kbk-Supervisor')
            department_to_highlight = issuedshot.department
            shot = Shot2.objects.get(shot_name=issuedshot.shot_name)
            # shot.dependency = shot.dependency.replace(department_to_highlight, f'<span class="highlight">{department_to_highlight}</span>')
            shot.save()
  
        else:
            Shot2.objects.filter(shot_name=issuedshot.shot_name).update(work_status='Assigned')
            department_to_highlight = issuedshot.department
            shot = Shot2.objects.get(shot_name=issuedshot.shot_name)
            # shot.dependency = shot.dependency.replace(department_to_highlight, f'<span class="highlight">{department_to_highlight}</span>')
            #shot.save()
            depnote_instance, created = ShotDepNote.objects.get_or_create(shot=shot)
            depnotes = depnote_instance.depnotes or []
            if department_to_highlight not in depnotes:
                depnotes.append(department_to_highlight)
                depnote_instance.depnotes = depnotes
                depnote_instance.save()


        eta = issuedshot.eta
        received_date = None
        issdate = issuedshot.issuedate
        overdue_days = 0
        manday = 0

        if (issuedshot.work_status == 'DONE' or issuedshot.work_status == 'READY FOR REVIEW' or issuedshot.work_status == 'HOLD') and \
           (not hasattr(issuedshot, 'received_date') or issuedshot.received_date is None):
            received_date = today
            issuedshot.received_date = received_date
            issuedshot.save()

        if issuedshot.received_date:
            received_date = issuedshot.received_date
            manday = (received_date - issdate).days

            if received_date > eta:
                overdue_days = (received_date - eta).days
            issuedshot.overdue = overdue_days
            issuedshot.manday = manday
            issuedshot.save()
        else:
            issuedshot.overdue = 0
            issuedshot.manday = (today - issdate).days
            issuedshot.save()

        if issuedshot.work_status != 'DONE' and issuedshot.work_status != 'READY FOR REVIEW':
            if today > eta:
                overdue_days = (today - eta).days
                issuedshot.overdue = overdue_days
            else:
                issuedshot.overdue = 0
            manday = (today - issdate).days
            issuedshot.manday = manday
            issuedshot.save()
        
        if issuedshot.work_status == 'HOLD':
            issuedshot.manday = 0
            issuedshot.overdue = 0
            issuedshot.save()
        
        artists = StudentExtra.objects.filter(department=issuedshot.department)
        t = (issuedshot.artist,
             issuedshot.project_name,
             issuedshot.shot_name,
             issuedshot.department,
             issuedshot.issuedate,
             issuedshot.eta,
             issuedshot.work_status,
             issuedshot.note,
             issuedshot.content,
             issuedshot.overdue,
             issuedshot.manday,
             issuedshot.id,
             issuedshot.received_date,
             issuedshot.shot_version,
             issuedshot.work_description,
             issuedshot.image1,
             issuedshot.kbk_image,
             )
        li.append(t)
    context = {'li': li, 'issuedshots':issuedshots}
    return render(request, 'user/viewissuedshot.html', context)

############################################################################################################################################

@login_required(login_url='adminlogin')                                                                             # Delete Assigned shot
@user_passes_test(is_admin)
def deleteissuedshot_view(request, pk):
    shot_obj = get_object_or_404(IssuedShot, pk=pk)
    shot_obj.delete()
    messages.success(request, 'Assigned shot removed successfully!')
    return redirect('viewissuedshot')


####################################################################################################################################################
#                                                                         4) MANAGEMENT     
####################################################################################################################################################

@login_required(login_url='adminlogin')                                                                                  # All Shot for management
def allshot_view1(request):
    shots = Shot2.objects.filter(work_status='Assigned').order_by('shot_name')
    paginator = Paginator(shots, 25)
    page = request.GET.get('page')
    shots = paginator.get_page(page) 
    context = {'shots': shots}
    return render(request, 'user/mang_message1.html', context)

####################################################################################################################################################
                                                                               
def searchshot_mang_view(request):                                                                                       # Search All Shot for Management
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            shots = Shot2.objects.filter(
                Q(project_name__istartswith=query) |
                Q(shot_name__istartswith=query) |
                Q(work_status__istartswith=query) )
            return render(request, 'user/search3.html', {'shots': shots})
    return render(request, 'user/search3.html') 
    
####################################################################################################################################################

@login_required(login_url='adminlogin')                                                                                 # Final Management Approved Shot
def final_approved_shot(request, shot_id):
    shot = Shot2.objects.get(pk=shot_id)
    #shot.internal_status = f'APPROVED (by {request.user.username})'
    #shot.internal_status = f'APPROVED'
    shot.internal_status = f'Approved By Sup'
    version = shot.shot_version
    approve = Approve(shot=shot, approved_by=request.user, version=version)
    approve.save()
    shot.save()
    messages.success(request, f'Shot (Version-{version}) Approved by {request.user.first_name} {request.user.last_name}.')
    return redirect('mang_message1')

#############################################################################################################################################
#################################################################    B) ARTIST PORTAL       #################################################
############################################################################################################################################# 


@login_required(login_url='studentlogin')                                                                          # All Project view to artist
def allproject_view_artist(request):
    projects = Shot2.objects.values('project_name').annotate(num_shots=Count('project_name')).order_by('project_name')
    context = {'projects': projects}
    return render(request, 'user/allproject_artist.html', context)

###############################################################################################################################################

@login_required(login_url='studentlogin')                                                                        # All shot by selected project - artist
def project_shots_view1(request, project_name): 
    shots = Shot2.objects.filter(project_name=project_name).order_by('shot_name')
    project_added_date = shots.first().date_started
    project_TGT_Date = shots.first().eta
    
    items_per_page = 30
    paginator = Paginator(shots, items_per_page)
    page = request.GET.get('page')

    try:
        shots = paginator.page(page)
    except PageNotAnInteger:
        shots = paginator.page(1)
    except EmptyPage:
        shots = paginator.page(paginator.num_pages)
        
    context = {'project_name': project_name, 'shots': shots, 'project_added_date': project_added_date, 'project_TGT_Date': project_TGT_Date}
    return render(request, 'user/pshots1.html', context)

###############################################################################################################################################

#@login_required(login_url='studentlogin')                                                                       #  Shot review/approval info 
# def get_review_approval_info(request, shot_id):
#     shot = Shot2.objects.get(pk=shot_id)
#     review_info = shot.get_reviews().order_by('version')
#     approve_info = shot.get_approves().order_by('version')
#     history_entries = ShotStatusHistory.objects.filter(shot=shot).order_by('change_date')
#     versions = Shot2.objects.filter(project_name=shot.project_name, shot_name=shot.shot_name).values_list('shot_version', flat=True).distinct()

#     context = {'review_info': review_info, 'approve_info': approve_info, 'history_entries': history_entries, 'versions': versions}
#     return render(request,'user/shotinfo.html', context)


@login_required(login_url='studentlogin')
def get_review_approval_info(request, shot_id):
    shot = Shot2.objects.get(pk=shot_id)
    review_info = shot.get_reviews().order_by('version')
    approve_info = shot.get_approves()
    history_entries = ShotStatusHistory.objects.filter(shot=shot).order_by('change_date')

    versions = list(set(review_info.values_list('version', flat=True)) | set(approve_info.values_list('version', flat=True)))
    versions.sort()

    selected_version = request.GET.get('version', versions[0] if versions else None)

    filtered_review_info = review_info.filter(version=selected_version)
    filtered_approve_info = approve_info.filter(version=selected_version)

    context = {
        'review_info': filtered_review_info,
        'approve_info': filtered_approve_info,
        'history_entries': history_entries,
        'versions': versions,
        'selected_version': selected_version,
    }
    return render(request, 'user/shotinfo.html', context)
#############################################################################################################################################

@login_required(login_url='studentlogin')                                                                       # Shot Assigned By Artist
def viewissuedshotbyartist_view(request):
    artist = StudentExtra.objects.filter(user_id=request.user.id)
    artist_name = artist[0].get_name  
    issuedshots = IssuedShot.objects.filter(artist=artist_name, department=artist[0].department).order_by('-id')
    li1 = []
    for issuedshot in issuedshots:
        issdate = issuedshot.issuedate
        t = (
            issuedshot.artist, 
            issuedshot.department, 
            issuedshot.project_name, 
            issuedshot.shot_name, 
            issdate,
            issuedshot.eta,
            issuedshot.note,
            issuedshot.work_status,
            issuedshot.shot_version,
            issuedshot.work_description,
            issuedshot.image1,
            issuedshot.kbk_image,
        )
        li1.append(t)

    context = {'li1': li1}
    return render(request, 'user/viewissuedshotbyartist.html', context)

#################################################################################################################################################

@login_required(login_url='studentlogin')                                                                            # Search Shot Assigned to Artist
def searchissuedshotbyartist_view(request):
    artist = StudentExtra.objects.filter(user_id=request.user.id)
    artist_name = artist[0].get_name  
    query = request.GET.get('q')
    issuedshots = IssuedShot.objects.filter(
        Q(artist=artist_name) & Q(department=artist[0].department) & Q(Q(project_name__icontains=query) | Q(shot_name__icontains=query))).order_by('-id')
    li1 = []

    for issuedshot in issuedshots:
        issdate = issuedshot.issuedate
        t = (
            issuedshot.artist,
            issuedshot.department, 
            issuedshot.project_name, 
            issuedshot.shot_name, 
            issdate,
            issuedshot.eta,
            issuedshot.note,
            issuedshot.work_status,)
        li1.append(t)

    context = {'li1': li1}
    return render(request, 'user/search4.html', context)

##############################################################################################################################################

@login_required(login_url='studentlogin')                                                                                 # Send Shot Status     
def sendfeedback_view(request):
    form = SendFeedbackForm()
    if request.method == 'POST':
        form = SendFeedbackForm(request.POST,request.FILES)
        if form.is_valid():
            d1           = form.save(commit=False)
            d1.artist    = form.cleaned_data['artist']
            project_name = form.cleaned_data['project_name']
            shot_name    = form.cleaned_data['shot_name']
            shot_version = form.cleaned_data['shot_version']
            issued_shots = IssuedShot.objects.filter(project_name=project_name, shot_name=shot_name, shot_version=shot_version)

            if issued_shots.exists():
                authorized_shot = None
                for issued_shot in issued_shots:
                    if issued_shot.artist == d1.artist:
                        authorized_shot = issued_shot
                        break

                if authorized_shot:
                    if authorized_shot.work_status == 'DONE':
                        messages.error(request, 'Work status has already been sent to DONE for this shot.')
                    else:
                        d1.work_status              = form.cleaned_data['work_status']
                        authorized_shot.work_status = d1.work_status

                        if 'image1' in request.FILES:
                            d1.image1 = request.FILES['image1'] 

                        authorized_shot.save()
                        d1.issued_shot              = authorized_shot
                        d1.save()
                        messages.success(request, 'Shot status sent successfully.')
                        return redirect('viewissuedshotbyartist')
                else:
                    messages.error(request, 'You are not authorized to send shot status for this shot.')
            else:
                form.add_error('shot_name', 'This shot not found with the given project.')
    context = {'form': form}
    return render(request, 'user/addfeedback.html', context)

#################################################################################################################################################

@login_required(login_url='studentlogin') 
def artist_portal(request):
    messages1 = ArtistMessage.objects.all().order_by('-date_sent')
    projects = {}

    for mes in messages1:
        project_name = mes.shot.project_name  
        if project_name not in projects:
            projects[project_name] = {'count': 1, 'shots': [mes.shot]}
        else:
            projects[project_name]['count'] += 1
            projects[project_name]['shots'].append(mes.shot)

    if request.method == 'POST':
        project_name_clicked = request.POST.get('project_name_clicked')
        if project_name_clicked in projects:
            selected_project = projects[project_name_clicked]
            context = {'projects': projects, 'selected_project': selected_project}
            return render(request, 'user/message.html', context)

    context = {'projects': projects}
    return render(request, 'user/message.html', context)



#############################################################################################################################################
#################################################################    Mandays PORTAL       ###################################################
############################################################################################################################################# 


@login_required(login_url='adminlogin') 
def issued_shots_with_departments(request):
    issued_shots = IssuedShot.objects.values('shot_name', 'department').annotate(total_manday=Sum('manday'), total_overdue=Sum('overdue')).order_by('shot_name')
    shot_departments = {}

    for shot in issued_shots:
        shot_name  = shot['shot_name']
        department = shot['department']
        manday     = shot['total_manday']
        overdue    = shot['total_overdue']

        if shot_name not in shot_departments:
            shot_departments[shot_name] = {'departments': {}, 'total_manday': 0, 'total_overdue': 0}

        shot_departments[shot_name]['departments'][department] = {'manday': manday, 'overdue': overdue}
        shot_departments[shot_name]['total_manday'] += manday
        shot_departments[shot_name]['total_overdue'] += overdue

    context = {'shot_departments': shot_departments, 'issued_shots':issued_shots}
    return render(request, 'user/mandays.html', context)

#############################################################################################################################################
#################################################################    Summery PORTAL       ###################################################
############################################################################################################################################# 


status_colors = {
    'YTS': 'red',
    'WIP': 'Cyan',
    'REVIEWED': 'hotpink',
    'HOLD': 'yellow',
    'READY FOR REVIEW': 'green',
    'Assigned' : 'orange',
    'Not Assigned' : 'gray',
    'Kbk-Internal' : 'blue',
}



def generate_pie_chart(labels, counts, title, status_colors):
    non_zero_counts = [count for count in counts if count > 0]
    non_zero_labels = [label for i, label in enumerate(labels) if counts[i] > 0]

    if not non_zero_counts:
        return None
    
    colors = [status_colors[label] for label in non_zero_labels]
    plt.figure(figsize=(6, 6))
    plt.pie(non_zero_counts, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(title, fontsize=18 )
    plt.legend(labels=non_zero_labels, loc='upper right')
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format='png')
    plt.close()
    chart_data = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')
    return chart_data
 


@login_required(login_url='adminlogin') 
def summery_allshots(request):
    shot2_counts                 = Shot2.objects.count()
    issuedshot_counts            = IssuedShot.objects.values('shot_name').annotate(count=Count('shot_name')).count()

    yts_count                    = Shot2.objects.filter(internal_status='YTS').count()
    wip_count                    = Shot2.objects.filter(internal_status='WIP').count()
    reviewed_count               = Shot2.objects.filter(internal_status='REVIEWED').count()
    hold_count                   = Shot2.objects.filter(internal_status='HOLD').count()
    ready_for_review_count       = Shot2.objects.filter(internal_status='READY FOR REVIEW').count()
    assigned_count               = Shot2.objects.filter(work_status='Assigned').count()
    not_assigned_count           = Shot2.objects.filter(work_status='Not Assigned').count()

    issued_assigned_count        = IssuedShot.objects.filter(work_status='Assigned').count()
    issued_reassigned_count      = IssuedShot.objects.filter(work_status='Kbk-Internal').count()
    issued_readyforreview_count  = IssuedShot.objects.filter(work_status='READY FOR REVIEW').count()
    issued_hold_count            = IssuedShot.objects.filter(work_status='HOLD').count()
    issued_wip_count             = IssuedShot.objects.filter(work_status='WIP').count()
    
    
    i_labels = ['YTS', 'WIP', 'REVIEWED', 'HOLD', 'READY FOR REVIEW']
    i_counts = [yts_count, wip_count, reviewed_count, hold_count,  ready_for_review_count]
    chart_data1 = generate_pie_chart(i_labels, i_counts, 'Internal Status', status_colors)

    w_labels = ['Assigned', 'Not Assigned']
    w_counts = [assigned_count, not_assigned_count]
    chart_data2 = generate_pie_chart(w_labels, w_counts, 'Assignment Status', status_colors)

    iss_labels = [ 'WIP', 'Assigned', 'Kbk-Internal', 'HOLD', 'READY FOR REVIEW']
    iss_counts = [ issued_wip_count, issued_assigned_count, issued_reassigned_count, issued_hold_count, issued_readyforreview_count]
    chart_data3 = generate_pie_chart(iss_labels, iss_counts, 'Assigned Shot', status_colors)

    context = {
        'shot2_counts': shot2_counts,
        'issuedshot_counts': issuedshot_counts,
        'yts_count': yts_count,
        'wip_count': wip_count,
        'reviewed_count': reviewed_count,
        'hold_count': hold_count,
        'ready_for_review_count': ready_for_review_count,
        'assigned_count': assigned_count,
        'not_assigned_count': not_assigned_count,
        'issued_assigned_count': issued_assigned_count,
        'issued_reassigned_count': issued_reassigned_count,
        'issued_readyforreview_count': issued_readyforreview_count,
        'issued_hold_count': issued_hold_count,
        'issued_wip_count': issued_wip_count,
        'chart_data1': chart_data1,
        'chart_data2': chart_data2,
        'chart_data3': chart_data3 }

    return render(request, 'user/summery.html', context)

#############################################################################################################

@login_required(login_url='adminlogin') 
def shot_status_history_view(request, shot_id):
    shot = Shot2.objects.get(pk=shot_id)
    history_entries = ShotStatusHistory.objects.filter(shot=shot).order_by('change_date')

    context = {'shot': shot, 'history_entries': history_entries}
    return render(request, 'user/internal.html', context)


