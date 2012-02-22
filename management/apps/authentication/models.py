#!/usr/bin/env python
# vim: set ts=4 sw=4 sts=4 et:
#=======================================================================
# Copyright (C) 2011 Alex Boonstra at OSSO B.V.
# This file is part of ticket-tracker.
#
# ticket-tracker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ticket-tracker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ticket-tracker. If not, see <http://www.gnu.org/licenses/>.
#=======================================================================

import imp
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.importlib import import_module


class UserProfile(models.Model):
    '''
    UserProfile class which will define restriction to queue's in the future
    '''
    user = models.OneToOneField(User, unique=True)

    def __unicode__(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user.username

def createUserProfile(sender, instance, **kwargs):
    '''
    Create a UserProfile object for the new created user each time a new user is created
    '''
    UserProfile.objects.get_or_create(user=instance)

    for app in settings.INSTALLED_APPS:
        try:
            '''
            Try to get the path of the installed app so wen can check if this app has a register file
            '''
            app_path = import_module(app).__path__
        except AttributeError:
            continue
        
        try:
            '''
            Check if the application has a register file, if it does, we set the view
            permissions for the newly created user
            '''
            imp.find_module('register', app_path)
            app_label = import_module(app).__name__.split('.')[-1]
            content_type = ContentType.objects.get(app_label=app_label)
            # Note that view permissions are set for each model for this project when we syncdb
            # This is not nativly supported by django.
            # see management/__init__.py for more information
            perm = Permission.objects.get(content_type=content_type, name='Can view %s' % app_label)
            instance.user_permissions.add(perm)
            instance.save()
        except:
            continue 


models.signals.post_save.connect(createUserProfile, sender=User)
