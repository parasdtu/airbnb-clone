from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = " This command helps create all amenities"

    def handle(self, *args, **options):
        facilities = [
            "Free parking on premises",
            "Gym",
            "Hot tub",
            "Pool",
        ]

        for f in facilities:
            room_models.Facility.objects.create(name=f)

        # writes to standard output in green wih success, red with error, yellow with warning
        self.stdout.write(self.style.SUCCESS("Facilities created!"))
