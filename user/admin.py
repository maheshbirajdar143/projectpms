from django.contrib import admin
from .models import *

####################################################################
admin.site.register(EmailAddress)
admin.site.register(UserActivity)

#####################################################################

class Shot2Admin(admin.ModelAdmin):
    pass
admin.site.register(Shot2, Shot2Admin)

######################################################################

class ArtistInfoAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, ArtistInfoAdmin)

######################################################################

class IssuedShotAdmin(admin.ModelAdmin):
    pass
admin.site.register(IssuedShot, IssuedShotAdmin)

#######################################################################

class SendFeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(SendFeedback, SendFeedbackAdmin)

#######################################################################

class ArtistMessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(ArtistMessage, ArtistMessageAdmin)

######################################################################

