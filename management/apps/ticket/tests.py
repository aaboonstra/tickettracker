import datetime
from django.contrib.auth.models import User
from management.apps.ticket.models import Ticket, Queue
from tools.tests import TestCase

class TicketTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='test', password='test')
        self.queue = Queue.objects.create(title='testqueue')

    def test_crud_ticket(self):
        # create ticket
        Ticket.objects.create(
            title='test',
            description='test',
            assigned_to=self.user,
            date_due=datetime.datetime.today(),
            queue=self.queue,
        )

        # get ticket
        ticket = self.get_object_or_none(Ticket, title='test') 
        self.assertNotNone(ticket)

        # update ticket
        ticket.title = 'test2'
        ticket.save()
        # refetch the ticket
        ticket = self.get_object_or_none(Ticket, title='test2') 
        self.assertNotNone(ticket)
   
        # delete ticket
        ticket.delete()
        # try to refetch the ticket
        ticket = self.get_object_or_none(Ticket, title='test2')
        self.assertNone(ticket)

        # Test the callable classmethods
        open_ticket = Ticket.objects.create(
            title='open_test',
            description='test',
            assigned_to=self.user,
            date_due=datetime.datetime.today(),
            status=Ticket.OPEN_STATUS,
            queue=self.queue,
        )

        resolved_ticket = Ticket.objects.create(
            title='resolved_test',
            description='test',
            assigned_to=self.user,
            date_due=datetime.datetime.today(),
            status=Ticket.RESOLVED_STATUS,
            queue=self.queue,
        )

        closed_ticket = Ticket.objects.create(
            title='closed_test',
            description='test',
            assigned_to=self.user,
            date_due=datetime.datetime.today(),
            status=Ticket.CLOSED_STATUS,
            queue=self.queue,
        )

        tickets = self.queue.get_open_tickets()
        self.assertEqual(tickets[0], open_ticket)

        tickets = self.queue.get_resolved_tickets()
        self.assertEqual(tickets[0], resolved_ticket)

        tickets = self.queue.get_closed_tickets()
        self.assertEqual(tickets[0], closed_ticket)

        tickets = self.queue.get_all_tickets()
        self.assertEqual(True, open_ticket in tickets)
        self.assertEqual(True, resolved_ticket in tickets)
        self.assertEqual(True, closed_ticket in tickets)
