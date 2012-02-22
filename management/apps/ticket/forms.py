from django import forms
from management.apps.ticket.models import Ticket
from management.apps.userprofile.models import UserProfile


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = UserProfile.get_assignable_users()
    
    class Meta:
        model = Ticket
        fields = (
            'title',
            'queue',
            'description',
            'date_due',
            'status',
            'priority',
            'assigned_to',
        )
