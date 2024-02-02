from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


CHOICES1= [
    ('Roto', 'Roto'),
    ('Paint', 'Paint'),
    ('CG', 'CG'),
    ('Comp','Comp'),
    ('Production','Production'),
    ('Editor','Editor'),
    ('Matchmove','Matchmove'),
    ('MGFX','MGFX'),
    ('DMP','DMP'),
    ('Pipeline','Pipeline'),
    ('IT','IT'),
    ('HR','HR'),
    ('Account','Account'),
    ]

CHOICES1 = sorted(CHOICES1, key=lambda choice: choice[1])



CHOICES2= [
    ('Intern', 'Intern'),
    ('Trainee', 'Trainee'),
    ('Jr. Artist', 'Jr. Artist'),
    ('Sr. Artist', 'Sr. Artist'),
    ('TD','TD'),
    ('Data IO','Data IO'),
    ('System Admin', 'System Admin'),
    ('Coordinator', 'Coordinator'),
    ('Team Lead','Team Lead'),
    ('Supervisor','Supervisor'),
    ('Production Manager', 'Production Manager'),
    ('VFX Producer', 'VFX Producer'),
    ('VFX Head', 'VFX Head'),
    ]


CHOICES3= [
    ('Mr. Riaz Patel (VFX Head)', 'Mr. Riaz Patel (VFX Head)'),
    ('Mr. Abhishek Kulkarni (Production Manager)', 'Mr. Abhishek Kulkarni (Production Manager)'),
    ('Mr. Swapnil Kharche (VFX Producer)', 'Mr. Swapnil Kharche (VFX Producer)'),
    ('Mr. Kunal Salunkhe', 'Mr. Kunal Salunkhe'),
    ('Mr. Ranjan Sharma', 'Mr. Ranjan Sharma'),
    ('Mr. Swapnil Zambare', 'Mr. Swapnil Zambare'),
    ('Mr. Chinmay Deshpande', 'Mr. Chinmay Deshpande'),
    ('Mr. Akshay Yadav', 'Mr. Akshay Yadav'),
    ]

#CHOICES3 = sorted(CHOICES3, key=lambda choice: choice[1])

CHOICES4= [
    ('YTS', 'YTS'),
    ('WIP', 'WIP'),
    ('DONE', 'DONE'),
    ('HOLD', 'HOLD'),
    ('Not Assigned', 'Not Assigned'),
    ('Assigned', 'Assigned'),
    ]




CHOICES6= [
    ('Not Assigned', 'Not Assigned'),
    ('Assigned', 'Assigned'),
    ]

CHOICES7= [
    ('Ok', 'OK'),
    ('Pending', 'Pending'),
    ]
	
############################################################################################################################################

class EmailAddress(models.Model):                                                                                       # for os1 venv
    class Meta:
        app_label = 'allauth'

#############################################################################################################################################

class UserActivity(models.Model):                                                                                      # for online artist
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time  = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

#############################################################################################################################################

class StudentExtra(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    aid         = models.IntegerField(unique=True)
    department  = models.CharField(max_length=100, choices=CHOICES1)
    designation = models.CharField(max_length=100, choices=CHOICES2)
    reporting   = models.CharField(max_length=100, choices=CHOICES3)

    def __str__(self):
        return str(self.department)
    
    def __str__(self):
        return str(self.get_name)
    
    @property
    def get_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    @property
    def getuserid(self):
        return self.user.aid


class AdminExtra(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    aid         = models.IntegerField(unique=True)
    department  = models.CharField(max_length=100, choices=CHOICES1)
    designation = models.CharField(max_length=100, choices=CHOICES2)

    def __str__(self):
        return str(self.department)
    
    def __str__(self):
        return str(self.get_name)
    
    @property
    def get_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    @property
    def getuserid(self):
        return self.user.aid
#######################################################################################################################################################

class Shot2(models.Model):
    project_name     = models.CharField(max_length=255, verbose_name='Project Name')
    shot_name        = models.CharField(max_length=2040, verbose_name='Shot Name')
    work_description = models.CharField(max_length=2550, verbose_name='Scope of Work')
    date_started     = models.DateTimeField(default=timezone.now, verbose_name='Date Created (Y-M-D)')
    eta              = models.DateField(null=True, blank=True,default=None, verbose_name='TGT Date (y-m-d)')                              # YYYY-MM-DD
    dependency       = models.TextField(verbose_name='Dependency')
    work_status      = models.CharField(max_length=255,choices=CHOICES6, verbose_name='Assignment', default='Not Assigned')
    final_status     = models.CharField(max_length=255,null=True, blank=True, verbose_name='Final Status', default='N/A')
    internal_status  = models.CharField(max_length=255,null=True, blank=True, verbose_name='Internal Status', default='YTS')
    remark           = models.CharField(max_length=1000,null=True, blank=True, verbose_name='Remark', default='N/A')
    client_status    = models.CharField(max_length=255,null=True, blank=True, verbose_name='Client Status', default='N/A')
    added_column     = models.JSONField(null=True, blank=True,default=dict)
    #shot_version     = models.IntegerField(null=True, blank=True, verbose_name='Version No.', default=1)
    shot_version     = models.CharField(max_length=5, null=True, blank=True, verbose_name='Version No.', default='V000')
    comp_status      = models.CharField(max_length=510,choices=CHOICES7, verbose_name='Comp Status', default='Pending')
    column_order     = models.TextField()
    issued_date      = models.DateTimeField(null=True, blank=True, verbose_name='Reviewed Date')
    issued_by        = models.CharField(max_length=255,null=True, blank=True, default='N/A')
    depnote          = models.CharField(max_length=255, null=True, blank=True, verbose_name='Department Note')                      # assigned all department
    recdepnote       = models.CharField(max_length=255, null=True, blank=True, verbose_name='Received Department Note')
    department       = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.project_name 
    
    def clean(self):                                          
        existing_shots = Shot2.objects.filter(project_name=self.project_name,shot_name=self.shot_name).exclude(id=self.id)  
        if existing_shots.exists():
            raise ValidationError("This shot has already been added in the system.")

    def save(self, *args, **kwargs): 
        self.clean()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        is_new_shot = self._state.adding
        super().save(*args, **kwargs)
        if is_new_shot:
            message = f"New shot '{self.shot_name}' has been added to the project '{self.project_name}' ."
            ArtistMessage.objects.create(shot=self, message=message)

    def get_reviews(self):
        return Review.objects.filter(shot=self).order_by('-reviewed_date')
    
    def get_approves(self):
        return Approve.objects.filter(shot=self).order_by('-approved_date')
    

    # def save(self, *args, **kwargs):
    #     is_new_shot = self._state.adding

    #     if is_new_shot or ('update_fields' in kwargs and 'internal_status' in kwargs['update_fields']):
    #         super().save(*args, **kwargs)
    #         ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)
    #     elif not is_new_shot and self.internal_status != self._state.adding:
    #         existing_status = ShotStatusHistory.objects.filter(shot=self, internal_status=self.internal_status).exists()
    #         if existing_status:
    #             pass
    #         else:
    #             super().save(*args, **kwargs)
    #             ShotStatusHistory.objects.create(shot=self, internal_status=self.internal_status)
    #     else:
    #         super().save(*args, **kwargs)


#####################################################################################################################################################

class ShotDepNote(models.Model):
    shot        = models.ForeignKey(Shot2, on_delete=models.CASCADE, related_name='dep_notes')
    depnotes    = models.JSONField(null=True, blank=True, default=list, verbose_name='Department Notes')
    recdepnotes = models.JSONField(null=True, blank=True, default=dict, verbose_name='Received Department Notes')
    recdates    = models.DateField(null=True, blank=True, verbose_name='Date Received')

#####################################################################################################################################################

class ShotStatusHistory(models.Model):
    shot            = models.ForeignKey(Shot2, on_delete=models.CASCADE, related_name='status_history')
    internal_status = models.CharField(max_length=255)
    change_date     = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.shot.shot_name} - {self.internal_status} - {self.change_date.strftime('%m/%d/%Y')}"

#######################################################################################################################################################

class Review(models.Model):
    shot          = models.ForeignKey(Shot2, on_delete=models.CASCADE)
    reviewed_by   = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_date = models.DateTimeField(auto_now=True)
    #version       = models.IntegerField(default=1)
    version       = models.CharField(max_length=5, null=True, blank=True, verbose_name='Version No.', default='V0000')

#######################################################################################################################################################

class Approve(models.Model):
    shot           = models.ForeignKey(Shot2, on_delete=models.CASCADE)
    approved_by    = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_date  = models.DateTimeField(auto_now=True)
    #version        = models.IntegerField(default=1)
    version        = models.CharField(max_length=5, null=True, blank=True, verbose_name='Version No.', default='V0000')

#######################################################################################################################################################

class ShotHistory(models.Model):
    shot           = models.ForeignKey(Shot2, on_delete=models.CASCADE)
    field_name     = models.CharField(max_length=255)
    previous_value = models.CharField(max_length=255, null=True, blank=True, default='')
    updated_value  = models.TextField()
    updated_by     = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at     = models.DateTimeField(auto_now_add=True)

####################################################################################################################################################   
   
class IssuedShot(models.Model):
    artist           = models.CharField(max_length=255)
    project_name     = models.CharField(max_length=255)
    shot_name        = models.CharField(max_length=255)
    #shot_version     = models.IntegerField(null=True, blank=True, verbose_name='Version No.')
    shot_version     = models.CharField(max_length=255,  null=True, blank=True, verbose_name='Version No.', default='V000')
    work_description = models.CharField(max_length=2550, verbose_name='Scope of Work')
    department       = models.CharField(max_length=100)
#    issuedate        =models.DateField(auto_now_add=True)
    issuedate        = models.DateField(null=True, blank=True, default=None)
    eta              = models.DateField(null=True, blank=True, default=None)
    work_status      = models.CharField(max_length=255, choices=CHOICES4, verbose_name='Shot Status')
    note             = models.CharField(max_length=2000, null=True, blank=True, default=None)
    content          = models.CharField(max_length=2000, null=True, blank=True, default=None)
    overdue          = models.IntegerField(null=True, blank=True, default=0)
    manday           = models.IntegerField(null=True, blank=True, default=0)
    received_date    = models.DateField(null=True, blank=True, default=None)
    image1           = models.ImageField(upload_to='annot_images/', null=True, blank=True,default=None)
    kbk_image        = models.ImageField(upload_to='kbk_images/', null=True, blank=True,default=None)
    
    def __str__(self):
        return  self.shot_name

#########################################################################################################################################################

class SendFeedback(models.Model):
    artist       = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    shot_name    = models.CharField(max_length=255)
    department   = models.CharField(max_length=255)
    work_status  = models.CharField(max_length=255, choices = CHOICES4)
    content      = models.CharField(max_length=2000, verbose_name='Comment')
#    date_posted  = models.DateTimeField(default=timezone.now, verbose_name='Date (Y-M-D)')
    issued_shot  = models.ForeignKey(IssuedShot, on_delete=models.CASCADE, null=True, blank=True)
    #shot_version = models.IntegerField(null=True, blank=True, verbose_name='Version No.')
    shot_version = models.CharField(max_length=100,null=True, blank=True, verbose_name='Version No.')
    image1       = models.ImageField(upload_to='annot_images/', null=True, blank=True)

    def __str__(self):
        return self.work_status
    
    
    def clean(self):
        super().clean()
        try:
            Shot2.objects.get(project_name=self.project_name, shot_name=self.shot_name)
        except Shot2.DoesNotExist:
            raise ValidationError("Invalid shot name.")
        

@receiver(post_save, sender=SendFeedback)
def update_shot2_work_status(sender, instance, **kwargs):
    if instance.issued_shot:
        IssuedShot.objects.filter(
            artist       = instance.issued_shot.artist,
            project_name = instance.issued_shot.project_name,
            shot_name    = instance.issued_shot.shot_name,
            shot_version = instance.issued_shot.shot_version).update( work_status=instance.work_status, content=instance.content, image1=instance.image1)
        
    if instance.issued_shot:
        IssuedShot.objects.filter(
            artist       = instance.issued_shot.artist,
            project_name = instance.issued_shot.project_name,
            shot_name    = instance.issued_shot.shot_name,
            shot_version = instance.issued_shot.shot_version).update(shot_version=instance.shot_version)
        
        Shot2.objects.filter(
            project_name=instance.project_name, shot_name=instance.shot_name,).update(shot_version=instance.shot_version)

#########################################################################################################################################################

class ArtistMessage(models.Model):                                                       # send popup message to artist portal 
    shot      = models.ForeignKey(Shot2, on_delete=models.CASCADE)
    message   = models.CharField(max_length=200)
    date_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message

###########################################################################################################################################################

class DepartmentIssuedShot(models.Model):
    shot_name  = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    mandays    = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.shot_name} - {self.department}"

##############################################################################################################################################################

    
