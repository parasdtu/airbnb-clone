import random
from django.core.management.base import BaseCommand
from reviews.models import Review
from users import models as users_models
from reviews import models as reviews_models
from rooms import models as rooms_models
from django_seed import Seed

# seed is a helper class that will create fake data


class Command(BaseCommand):

    help = " This command creates many fake reviews"

    # this one is for when you call the functions such as
    # "python manage.py seed_reviews"
    # you can add "--number 50" at the end to tell
    # to create 50 fake reviews
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="Enter how many fake reviews you want to create",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):

        seeder = Seed.seeder()

        # the number which was added in the above method
        # as arguments will be available here in options,
        # or defaults to 1 of --number is not set while calling the class
        number = options.get("number")

        all_users = users_models.User.objects.all()
        all_rooms = rooms_models.Room.objects.all()

        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda x: random.randint(1, 5),
                "communication": lambda x: random.randint(1, 5),
                "cleanliness": lambda x: random.randint(1, 5),
                "location": lambda x: random.randint(1, 5),
                "check_in": lambda x: random.randint(1, 5),
                "value": lambda x: random.randint(1, 5),
                "room": lambda x: random.choice(all_rooms),
                "user": lambda x: random.choice(all_users),
            },
        )

        seeder.execute()
        # writes to standard output in green wih success, red with error, yellow with warning
        self.stdout.write(self.style.SUCCESS(f"{number} Reviews created!"))
