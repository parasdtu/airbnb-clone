from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class FacilityAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    # mark safe was used to let django know that the image
    # html is safe
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width=50px src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


# this will help select photos of a room from the room admin itself
# instead of adding photos separately for a room
class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                ),
            },
        ),
        (
            "Times",
            {
                "fields": (
                    "check_in",
                    "check_out",
                    "instant_book",
                ),
            },
        ),
        (
            "Spaces",
            {
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
        (
            "More About The Space",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                ),
            },
        ),
        (
            "Last Details",
            {
                "fields": ("host",),
            },
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_facilities",
        "count_house_rules",
        "count_photos",
        "total_rating",
    )

    ordering = ("price",)

    # to be able to filter rooms by the instant book facility,
    # by city and by country
    list_filter = (
        "instant_book",
        "city",
        "room_type",
        "host__superhost",
        "amenities",
        "facilities",
        "country",
    )

    # can only add many to many fields here
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # will not display the entire list of users
    # instead one will select user by id
    # used for very long list
    raw_id_fields = ("host",)

    # enable a search field for searching
    search_fields = ("city", "host__username")

    def count_amenities(self, obj):
        print(obj.amenities.all())
        return obj.amenities.all().count()

    count_amenities.short_description = "Amenities"

    def count_facilities(self, obj):
        print(obj.facilities.all())
        return obj.facilities.all().count()

    count_facilities.short_description = "Facilities"

    def count_house_rules(self, obj):
        print(obj.house_rules.all())
        return obj.house_rules.all().count()

    count_house_rules.short_description = "House Rules"

    def count_photos(self, obj):
        print(obj.photos.all())
        return obj.photos.all().count()

    count_photos.short_description = "Number of photos"

    # this is called when admins saves a model
    # can be used to intercept
    # def save_model(self, request, obj, form, change):
    #     print(obj, change, form)
    #     return super().save_model(request, obj, form, change)


class RoomInline(admin.TabularInline):
    model = models.Room
