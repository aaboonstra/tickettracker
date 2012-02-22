# vim: set ts=4 sw=4 sts=4 et ai:
from django.contrib import admin
from management.apps.ticket.models import Ticket 


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('',)

admin.site.register(Ticket, TicketAdmin)
