import sys

from django.core.management.base import NoArgsCommand
from django.core.management.commands import cleanup

from django.contrib.sessions.models import Session

from prospecting.models import Prospect
from sentry.client.models import client as sentry


class Command(NoArgsCommand):
    help = "moves prospecting data from sessions into the database. Currently specific to DB sessions"
    
    def handle_noargs(self, *args, **kwargs):
        for s in Session.objects.all():
            # Note progress
            sys.stdout.write(".")
            sys.stdout.flush()

            try:
                prospect = Prospect.update_from_session(s)
                print("Updated from session: %s" % prospect)
            except ValueError:
                #sentry.create_from_exception()
                pass


        cleanup.Command().execute()
        print("done")
