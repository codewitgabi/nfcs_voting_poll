import os
from django.core.wsgi import get_wsgi_application
from threading import Thread

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VoteApp.settings")

from poll.service import add_voters_from_csv

application = get_wsgi_application()

# vercel config

app = application

thread = Thread(target=add_voters_from_csv)
thread.start()
