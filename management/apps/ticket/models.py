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

import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from tools.models import AbstractModel as Model


class Queue(Model):
    title = models.CharField(max_length=255)


class Ticket(Model):
    
    OPEN_STATUS = 'open'
    RESOLVED_STATUS = 'resolved'
    CLOSED_STATUS = 'closed'

    STATUS_CHOICES = (
        (OPEN_STATUS, _('Open')),
        (RESOLVED_STATUS, _('Resolved')),
        (CLOSED_STATUS, _('Closed')),
    )

    CRITICAL_PRIORITY = 'critical'
    HIGH_PRIORITY = 'high'
    MEDIUM_PRIORITY = 'medium'
    LOW_PRIORITY = 'low'

    PRIORITY_CHOICES = (
        (LOW_PRIORITY, settings.LOW_PRIORITY),
        (MEDIUM_PRIORITY, settings.MEDIUM_PRIORITY),
        (HIGH_PRIORITY, settings.HIGH_PRIORITY),
        (CRITICAL_PRIORITY, settings.CRITICAL_PRIORITY),
    )
 
    
    uuid = models.CharField(primary_key=True, editable=False, unique=True, max_length=32, default=lambda: uuid.uuid1().hex)
    title = models.CharField(max_length=255)
    queue = models.ForeignKey(Queue)
    description = models.TextField()
    date_due = models.DateField() #set default!?
    assigned_to = models.ForeignKey(User)
    status = models.CharField(choices=STATUS_CHOICES, default=OPEN_STATUS, max_length=63)
    priority = models.CharField(choices=PRIORITY_CHOICES, default=MEDIUM_PRIORITY, max_length=63)

    @classmethod
    def get_all_tickets(cls, queue):
        '''
        Given a queue, returns all tickets attached to the queue
        '''
        return cls.objects.filter(queue=queue).order_by('date_due')


    @classmethod
    def get_open_tickets(cls, queue):
        '''
        Given a queue, returns all open tickets attached to the queue
        '''
        return cls.objects.filter(queue=queue, status=Ticket.OPEN_STATUS).order_by('date_due')

    @classmethod
    def get_resolved_tickets(cls, queue):
        '''
        Given a queue, returns all resolved tickets attached to the queue
        '''
        return cls.objects.filter(queue=queue, status=Ticket.RESOLVED_STATUS).order_by('date_due')

    @classmethod
    def get_closed_tickets(cls, queue):
        '''
        Given a queue, returns all closed tickets attached to the queue
        '''
        return cls.objects.filter(queue=queue, status=Ticket.CLOSED_STATUS).order_by('date_due')



Queue.get_all_tickets = lambda queue: Ticket.get_all_tickets(queue)
Queue.get_open_tickets = lambda queue: Ticket.get_open_tickets(queue)
Queue.get_resolved_tickets = lambda queue: Ticket.get_resolved_tickets(queue)
Queue.get_closed_tickets = lambda queue: Ticket.get_closed_tickets(queue)
