# vim: set ts=4 sw=4 sts=4 et ai:
from django.contrib import admin
from management.apps.userprofile.models import UserProfile 

admin.site.register(UserProfile)
