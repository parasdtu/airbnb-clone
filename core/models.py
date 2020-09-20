from django.db import models

# Create your models here.
# all other models except user will have a timestamp property
# so instead of creating in all we have created a core model
# which all other will extend from
class TimeStampedModel(models.Model):
    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # We don't model to go to the database
    # hence we make this class abstract as below
    class Meta:
        abstract = True
