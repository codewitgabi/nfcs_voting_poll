import os
from django.conf import settings
import csv
import django

django.setup()
from .models import Voter


def add_voters_from_csv():
    """
    Add those who filled the biodata form to the list of voters.
    """
    BASE_DIR = settings.BASE_DIR
    csv_file = os.path.join(BASE_DIR, "data.csv")

    with open(csv_file, "r") as file:
        content = csv.reader(file)
        for data in content:
            name, phone = data[1], data[9]
            try:
                voter = Voter.objects.create(name=name.strip(), phone=phone.strip())
                voter.save()
            except:
                pass
