from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import render


CHOICES1= [
    ('Roto', 'Roto'),
    ('Paint', 'Paint'),
    ('Comp','Comp'),
    ('CG','CG'),
    ('Production','Production'),
    ('Editor','Editor'),
    ('MGFX','MGFX'),
    ('DMP','DMP'),
    ('Pipeline','Pipeline'),
    ]

CHOICES1 = sorted(CHOICES1, key=lambda choice: choice[1])

CHOICES2= [
    ('Intern', 'Intern'),
    ('Artist', 'Artist'),
    ('TD','TD'),
    ('Coordinator', 'Coordinator'),
    ('Team Lead','Team Lead'),
    ('Supervisor','Supervisor'),
    ('HOD','HOD')
    ]


CHOICES3= [
    ('Mr. Riaz patel', 'Mr. Riaz patel'),
    ('Mr. Abhishek', 'Mr. Abhishek'),
    ('Mr. Swapnil', 'Mr. Swapnil'),
    ('Mr. Vinay', 'Mr. Vinay'),
    ('Mr. Kunal', 'Mr. Kunal'),
    ('Mr. Balram', 'Mr. Balram'),
    ]


CHOICES4= [
    ('YTS', 'YTS'),
    ('WIP', 'WIP'),
    ('DONE', 'DONE'),
    ('Not Assigned', 'Not Assigned'),
    ('Assigned', 'Assigned'),
    ]


CHOICES6= [
    ('WIP', 'WIP'),
    ('DONE', 'DONE'),
    ('HOLD', 'HOLD'),
    ]

##################################################################################################################################

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model =User
		fields = ['email']

##################################################################################################################################

class UserRegisterForm(UserCreationForm):
    email       = forms.EmailField()
    uid         = forms.IntegerField(label='UID')
    department  = forms.CharField(label='Department', widget=forms.Select(choices=CHOICES1))
    designation = forms.CharField(label='Designation', widget=forms.Select(choices=CHOICES2))
    reporting   = forms.CharField(label='Reporting', widget=forms.Select(choices=CHOICES3))

    class Meta:
        model  = User
        fields = UserCreationForm.Meta.fields + ('email','uid', 'department','designation','reporting')


###################################################################################################################################

class AdminSigupForm(forms.ModelForm):
    email = forms.EmailField(label='Email (It should be : username@osvfx.in)')
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model  = User
        fields = ['first_name','last_name','username','email','password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        username1, domain1 = email.split('@', 1)

        if username1 != username or domain1 != 'osvfx.in':
            raise ValidationError('Invalid email format. Please use username@osvfx.in.')
        return email



class AdminExtraForm(forms.ModelForm):
    aid = forms.IntegerField(label='Emp ID')

    class Meta:
        model  = AdminExtra
        fields = ['aid','department','designation']

    def clean_aid(self):
        aid = self.cleaned_data['aid']
        if AdminExtra.objects.filter(aid=aid).exists():
            raise forms.ValidationError('Emp ID already exists.')
        return aid

###################################################################################################################################

class StudentSignupForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model  = User
        fields = ['first_name','last_name','username','email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        username1, domain1 = email.split('@', 1)

        if username1 != username or domain1 != 'osvfx.in':
            raise ValidationError('Invalid email format. Please use username@osvfx.in.')
        return email



class StudentExtraForm(forms.ModelForm):
    aid = forms.IntegerField(label='Emp ID')

    class Meta:
        model  = StudentExtra
        fields = ['aid','department','designation', 'reporting']

    def clean_aid(self):
        aid = self.cleaned_data['aid']
        if StudentExtra.objects.filter(aid=aid).exists():
            raise forms.ValidationError('Emp ID already exists.')
        return aid

####################################################################################################################################

class CustomDateInput(forms.DateInput):
    input_type = 'date'
    format     = '%d/%m/%Y'


class ShotForm(forms.ModelForm):
    eta          = forms.DateField(label='Project TGT Date', widget=CustomDateInput)
    shot_name    = forms.CharField(label='Shot Name', widget=forms.Textarea)
    dependency   = forms.MultipleChoiceField(
        label    = 'Dependency',
        widget   = forms.CheckboxSelectMultiple,
        choices  = CHOICES1,)

    class Meta:
        model  = Shot2
        fields = ['project_name','shot_name','work_description','date_started','eta','dependency','work_status']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.dependency:
            self.fields['dependency'].initial = self.instance.dependency.split(',')


    def clean_dependency(self):
        dependencies = self.cleaned_data['dependency']
        return ','.join(dependencies) 
    
#####################################################################################################################################

class EditShotForm(forms.ModelForm):
    dependency   = forms.MultipleChoiceField(
        label    = 'Dependency',
        widget   = forms.CheckboxSelectMultiple,
        choices  = CHOICES1,)
    
    class Meta:
        model  = Shot2
        fields = ['project_name','shot_name','shot_version','work_description','eta','work_status','dependency','internal_status','comp_status','remark','client_status']

    def clean_dependency(self):
        dependencies = self.cleaned_data['dependency']
        return ','.join(dependencies) 


class EditShotForm1(forms.ModelForm):    
    class Meta:
        model  = Shot2
        fields = ['work_description','eta','comp_status','remark','client_status']

######################################################################################################################################

class CustomDateInput(forms.DateInput):
    input_type = 'date'
    format     = '%d/%m/%Y'

#######################################################################################################################################

class IssuedShotForm(forms.Form):
    projectname1     = forms.ModelChoiceField(queryset = Shot2.objects.values_list('project_name', flat=True).distinct(),to_field_name="project_name",label='Project Name')
    shotname1        = forms.ModelChoiceField(queryset = Shot2.objects.values_list('shot_name', flat=True).distinct(),to_field_name="shot_name",label='Shot Name')
    #shotversion1     = forms.IntegerField(label='Shot Version')
    shotversion1     = forms.CharField(label='Shot Version')
    workdescription1 = forms.CharField(label='Scope of work')
    department1      = forms.CharField(label='Department', widget=forms.Select(choices=CHOICES1))
    artist1          = forms.ModelChoiceField(queryset=StudentExtra.objects.all().order_by('user__username'), label='Artist')
    issdate1         = forms.DateField(label='Issue Date', widget=CustomDateInput)
    eta1             = forms.DateField(label='Shot ETA', widget=CustomDateInput)
    note1            = forms.CharField(label='Feedback')
    kbk_image1       = forms.ImageField(label='kbk_img',required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department1'].label_from_instance = self.label_from_department_instance
        self.fields['issdate1'].initial = datetime.now().date()

    def label_from_department_instance(self, obj):
        return str(obj[1])  
    
    
    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department1')
        artist = cleaned_data.get('artist1')
        project_name = cleaned_data.get('projectname1')
        shot_name    = cleaned_data.get('shotname1')
        shot_version = cleaned_data.get('shotversion1')

        # if department and project_name and shot_name and shot_version:
        #     exist_shots = IssuedShot.objects.filter(
        #         department=department,
        #         project_name=project_name,
        #         shot_name=shot_name,
        #         shot_version=shot_version)
            
        #     if exist_shots.exists():
        #         exist_shots.delete()

        if department and artist:
            artist_department = artist.department
            if department != artist_department:
                raise forms.ValidationError("Artist does not belong to the selected department.")
            
        if artist and project_name and shot_name:
            existing_shots = IssuedShot.objects.filter(
                artist=artist,
                project_name=project_name,
                shot_name=shot_name,
                shot_version=shot_version)
            if existing_shots.exists():
                raise ValidationError(f"This shot version={shot_version} has already been issued to the same artist.")
            

    # def clean_shotversion1(self):
    #     shot_version = self.cleaned_data['shotversion1']
    #     if shot_version < 0:
    #         raise ValidationError("Shot Version must be a positive value")
    #     elif shot_version ==0 :
    #         raise ValidationError("Shot Version must be > 0")
    #     return shot_version
            
            
    def clean_issdate1(self):
        issdate1 = self.cleaned_data.get('issdate1')
        today = datetime.now().date()

        if issdate1 != today:
            raise forms.ValidationError("Issue date must be today.")
        return issdate1
    
    
    def clean_eta1(self):
        eta_date = self.cleaned_data['eta1']
        current_date = timezone.now().date()
        if eta_date < current_date:
            raise ValidationError("ETA must be today or greater than the today.")
        return eta_date
    

    def clean_shotname1(self):
        project_name = self.cleaned_data['projectname1']
        shot_name = self.cleaned_data['shotname1']
        if not Shot2.objects.filter(project_name=project_name, shot_name=shot_name).exists():
            raise ValidationError("This shot name is not available in the selected project.")
        return shot_name
    
######################################################################################################################################

class SendFeedbackForm(forms.ModelForm):
    project_name = forms.ModelChoiceField(queryset = Shot2.objects.values_list('project_name', flat=True).distinct(),to_field_name="project_name",label='Project Name')
    work_status  = forms.CharField(label='Work Status',widget=forms.Select(choices=CHOICES6))
    image1 = forms.ImageField(label='Upload Image/Annotation', required=False) 
    content  = forms.CharField(label='Add Comment')

    class Meta:
        model  = SendFeedback
        fields = ['artist','project_name','shot_name','work_status','content','shot_version','image1']

######################################################################################################################################

'''
def save(self, *args, **kwargs):
        is_new_shot = self._state.adding

        if is_new_shot or ('update_fields' in kwargs and 'internal_status' in kwargs['update_fields']):
            super().save(*args, **kwargs)
            ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)
        elif not is_new_shot and self.internal_status != self._state.adding:
            super().save(*args, **kwargs)
            ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)
        else:
            super().save(*args, **kwargs)
'''



'''
def save(self, *args, **kwargs):
        is_new_shot = self._state.adding  

        super().save(*args, **kwargs)

        if is_new_shot or ('update_fields' in kwargs and 'internal_status' in kwargs['update_fields']):
            ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)

        if not is_new_shot and self.internal_status != self._state.adding:
            ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)
'''




'''
def save(self, *args, **kwargs):
        is_new_shot = self._state.adding  

        super().save(*args, **kwargs)

        if is_new_shot or ('update_fields' in kwargs and 'internal_status' in kwargs['update_fields']):
            ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)
'''