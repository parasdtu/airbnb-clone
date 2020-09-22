import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from rooms.models import Room
from users import models as users_models
from rooms import models as rooms_models
from django_seed import Seed

# seed is a helper class that will create fake data


class Command(BaseCommand):

    help = " This command creates many fake rooms"

    # this one is for when you call the functions such as
    # "python manage.py seed_rooms"
    # you can add "--number 50" at the end to tell
    # to create 50 fake rooms
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="Enter how many fake rooms you want to create",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):

        seeder = Seed.seeder()

        # the number which was added in the above method
        # as arguments will be available here in options,
        # or defaults to 1 of --number is not set while calling the class
        number = options.get("number")

        # the third argument in add_entity is where
        # you want your specific rules
        # this will not work cuz we have users as foreign keys
        # seeder does not halp us with that
        # seeder.add_entity(
        #     Room,
        #     number,
        # )

        # hence we will have to randomly add users as custom fields
        # in room entity

        all_users = users_models.User.objects.all()
        all_room_types = rooms_models.RoomType.objects.all()
        seeder.add_entity(
            Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(all_room_types),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 10),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )

        # photo numbers from 5-35 as (5).webp

        # seeder.execute returs a dictionary of primary key pk
        # of the created elements
        # like this for 2 rooms {<class 'rooms.models.Room'>: [31, 32]}
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        print(len(created_clean))
        # created_clean is the list of primarry keys of the created rooms

        amenities = rooms_models.Amenity.objects.all()
        facilities = rooms_models.Facility.objects.all()
        rules = rooms_models.HouseRule.objects.all()
        # for every room that is created above
        # we get the room
        # and we add 5-10 room photos for that room
        for pk in created_clean:
            room = rooms_models.Room.objects.get(pk=pk)
            # print(room)
            for i in range(1, random.randint(7, 12)):
                photo = rooms_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/({random.randint(5,35)}).webp",
                )
                # print(f"{photo} was added to {room}")

            # this is how we work with many to many fields
            for a in amenities:
                magid_number = random.randint(0, 15)
                if magid_number % 2 == 0:
                    room.amenities.add(a)
                    # print(f"amenity {a} added")

            for a in facilities:
                magid_number = random.randint(0, 15)
                if magid_number % 2 == 0:
                    room.facilities.add(a)
                    # print(f"facility {a} added")

            for a in rules:
                magid_number = random.randint(0, 15)
                if magid_number % 2 == 0:
                    room.house_rules.add(a)
                    # print(f"rules {a} added")

        # writes to standard output in green wih success, red with error, yellow with warning
        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created!"))
