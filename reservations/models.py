from django.db import models
from core import models as core_models

# Create your models here.


class Reservation(core_models.TimeStampedModel):

    """ Reservation model definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING
    )

    # the below "user.User" directly makes use of User model
    # instead of importing that class and writing
    # users_models.User
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)

    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - {self.check_in}"