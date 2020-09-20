from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
# this class modifies how admin panel looks by adding
# used below annotation instead of at last=> admin.site.register(models.User, CustomUserAdmin)
# here again UserAdmin is the admin that django provides by default
# we are extending it to implement its functionality
# along with ours


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    # """ Custom User Admin """
    # commented cuz we will use django provided admin panel
    # list_display = ("username", "gender", "language", "currency", "superhost")
    # list_filter = ("language", "superhost", "currency")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )
