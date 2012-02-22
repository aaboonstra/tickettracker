from django.contrib import admin

from management.apps.authentication.models import UserProfile

admin.site.register(UserProfile)
