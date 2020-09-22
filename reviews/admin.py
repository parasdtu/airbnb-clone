from django.contrib import admin
from . import models

# . means from the same package i.e. reviews package
# meaning we import the reviews model class


# Register your models here.


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ review Admin Definition """

    list_display = ("__str__", "rating_average")
