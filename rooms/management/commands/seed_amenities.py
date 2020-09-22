from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = " This command helps create all amenities"

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop-friendly workspace",
            "TV",
            "Crib",
            "High chair",
            "Self check-in",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Private bathroom",
            "Piano",
        ]

        for a in amenities:
            room_models.Amenity.objects.create(name=a)

        # writes to standard output in green wih success, red with error, yellow with warning
        self.stdout.write(self.style.SUCCESS("Amenties created!"))
