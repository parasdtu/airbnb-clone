from django.db import models
from django_countries.fields import CountryField
from core import models as core_model
from users import models as users_model


# Create your models here.


class AbstractItem(core_model.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """ Room type definition """

    class Meta:
        verbose_name_plural = "Room Types"


class Amenity(AbstractItem):
    """ Amenity type definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility type definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Type definition """

    class Meta:
        verbose_name_plural = "House Rules"


class Room(core_model.TimeStampedModel):
    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    room_type = models.ForeignKey(
        RoomType, blank=True, on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    house_rules = models.ManyToManyField(HouseRule, blank=True)

    # Connecting room to a host user
    # cascade means if user deleted, delete their rooms as well
    host = models.ForeignKey(users_model.User, on_delete=models.CASCADE)

    # usually python will show the name of a room object as RoomObject1
    # we can override __str__ method to say what we want the name of
    # any toom object to be

    def __str__(self):
        return self.name


class Photo(core_model.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
