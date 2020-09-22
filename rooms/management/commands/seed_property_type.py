from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = " This command helps create all amenities"

    def handle(self, *args, **options):
        property_types = [
            "House",
            "Apartment",
            "Bed and breakfast",
            "Boutique hotel",
            "Bungalow",
            "Cabin",
            "Cottage",
            "Guest suite",
            "Guesthouse",
            "Hostel",
            "Hotel",
            "Loft",
            "Resort",
            "Serviced apartment",
            "Townhouse",
            "Villa",
        ]

        for f in property_types:
            room_models.RoomType.objects.create(name=f)

        # writes to standard output in green wih success, red with error, yellow with warning
        self.stdout.write(self.style.SUCCESS("Proerty types created!"))
