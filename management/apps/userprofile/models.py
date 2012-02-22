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

from django.contrib.auth.models import User
from django.db import models
from tools.models import AbstractModel as Model


class UserProfile(Model):
    user = models.OneToOneField(User, unique=True)
    assignable = models.BooleanField(default=False)

    @classmethod
    def get_assignable_users(cls):
        users = []
        for user in cls.objects.filter(assignable=True):
            users.append(user)
        return users

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


models.signals.post_save.connect(createUserProfile, sender=User)
