from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [

########################    ADMIN PORTAL   ####################################################### 

    path('logout/', LogoutView.as_view(template_name='user/index.html'),name='logout'),
    path('', home_view,name='h'),
    path('adminclick/', adminclick_view, name='adminclick'),
    path('studentclick/', studentclick_view, name='studentclick'),
    path('adminsignup', adminsignup_view, name='adminsignup'),
    path('studentsignup', studentsignup_view, name='studentsignup'),
    path('afterlogin', afterlogin_view, name='afterlogin'),
    path('allartist/', allartist_view, name='allartist1'),
    path('alladmin/', alladmin_view, name='alladmin1'),
    path('editartist/<int:id>/', editartist_view ,name='editartist'),
    path('changepass/', change_password, name='changepass'),
    path('search_all_admin/', search_shot2_admin, name='search_all_admin'),
    path('search_all_artist/', search_shot2_artist, name='search_all_artist'),
    path('online_artist/', logged_in_users, name='logged_in_artist'),
    path('userupdate/', UpdateUserProfile, name='userupdate'),

########################   1) PRODUCTION  ########################################################

    path('p1/', import_excel, name='importdata'),
    path('p2/', addproject_view, name='addproject'),
    path('p3/', allproject_view, name='allproject'),                                            # All Projects
    path('p4/<str:project_name>/', project_shots_view, name='pshots'),                          # Shot by project wise 
    path('p5/<str:project_name>/', addshot_project, name='addshot_project'),                    # Shot add inside project
    path('p6/<int:id>/', editshot_view ,name='editshot'),
    path('p7/', searchprojectshot_view, name= 'search1'),
    path('p8/<str:project_name>/', update_work_status1, name='update_work_status1'),
    path('p9/', update_dependency1, name='update_dependency1'),
    path('p10/<str:project_name>/', delete_project, name='delete_project'),                     # Delete Project   
    path('p11/<int:id>/', editshot_view1 ,name='editshot1'), 
    path('p12/<int:pk>/', deleteshot_view ,name='deleteshot'),
    path('p13/<int:shot_id>/', shot_history_view, name='shot_history'),

########################   2) TASK    ############################################################

    path('t1/', allshot_view, name='allshot'),  
    path('t1/<str:project_name>/', allshot_view, name='allshot_project'),
    path('t3/', searchshot_view, name= 'search'),
    path('t4/<int:shot_id>/', reviewed_shot, name='reviewed_shot'),
    path('t5/', re_issueshot_view, name='re_issueshot'),
    path('t6/', get_artists_by_department, name='get_artists_by_department'),
    path('t7/', re_issueshot_sup_view, name='re_issueshot_sup'),
    path('t8/', confirm_replace_shot, name='confirm_replace_shot'),

#########################  3) ARTIST  ###########################################################

    path('a1/', issueshot_view, name='issueshot'),
    path('a2/', viewissuedshot_view, name='viewissuedshot'),
    path('a3/<int:pk>/', deleteissuedshot_view, name='deleteissuedshot'),

########################   4) MANGMENT    #######################################################

    path('m1/', allshot_view1, name='mang_message1'),
    path('m2/', searchshot_mang_view, name= 'search3'),      
    path('m3/<int:shot_id>/', final_approved_shot, name='final_approved_shot'),

########################   5) MANDAY   ##########################################################

    path('manday/', issued_shots_with_departments, name='mandays'),

########################   6) SUMMERY    ########################################################

    path('s1/', summery_allshots, name='summery'), 

########################    ARTIST PORTAL   #####################################################

    path('ar2/', viewissuedshotbyartist_view, name='viewissuedshotbyartist'),
    path('ar3/', searchissuedshotbyartist_view, name= 'search4'),
    path('ar4/', sendfeedback_view, name='sendfeedback'),
    path('ar5/', artist_portal, name='popup_message'), 
    path('ar6/', allproject_view_artist, name='allproject_artist'),
    path('ar7/<str:project_name>/', project_shots_view1, name='pshots1'),  
    path('ar8/<int:shot_id>/', get_review_approval_info, name='get_review_approval_info'),
    path('shot/<int:shot_id>/', shot_status_history_view, name='internal'),
    path('shotdep/<int:id>/', shot_department_view, name='shotdep'),
    
]











'''                 replacing existing shot yes or no



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
                        department=department,
                    )

                    if existing_shots.exists():
                        # Shot already exists, ask for confirmation
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
                            },
                        )

                    # If there are no existing shots, create a new one
                    IssuedShot.objects.create(
                        artist=artist,
                        department=department,
                        shot_name=shot_name,
                        shot_version=request.POST.get('shotversion1'),
                        work_description=request.POST.get('workdescription1'),
                        project_name=project_name,
                        issuedate=request.POST.get('issdate1'),
                        eta=request.POST.get('eta1'),
                        note=request.POST.get('note1'),
                        kbk_image=kbk_image,
                        work_status='Assigned',
                    )

                    messages.success(request, f'Shot ({shot_name}) assigned successfully.')
                    return redirect('viewissuedshot')
    else:
        shot_name = request.GET.get('shot_name')
        project_name = request.GET.get('project_name')
        work_description = request.GET.get('work_description')

        if shot_name and project_name:
            form.initial['shotname1'] = shot_name
            form.initial['projectname1'] = project_name
            form.initial['workdescription1'] = work_description

    context['form'] = form
    return render(request, 'user/issueshot.html', context)




def confirm_replace_shot(request):
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
'''