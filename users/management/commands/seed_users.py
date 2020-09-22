from django.core.management.base import BaseCommand
from users.models import User
from django_seed import Seed

# seed is a helper class that will create fake data


class Command(BaseCommand):

    help = " This command creates many fake users"

    # this one is for when you call the functions such as
    # "python manage.py seed_users"
    # you can add "--number 50" at the end to tell
    # to create 50 fake users
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="Enter how many fake users you want to create",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):

        seeder = Seed.seeder()

        # the number which was added in the above method as arguments
        # will be available here in options, or defaults to 1 of --number is not set while calling the class
        number = options.get("number")

        # the third argument in add_entity is where
        # you want your specific rules
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
            },
        )

        seeder.execute()

        # writes to standard output in green wih success, red with error, yellow with warning
        self.stdout.write(self.style.SUCCESS("users created!"))
