import uuid

# this is for generating a random secret key for email verification
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils.html import strip_tags

# to send verification email to the user

from django.conf import settings


# Create your models here.
# AbstractUser is the default user that djago creates
# with all intial fields such as email, username, password, etc.
# inheriting this AbstractUser class helps us make our custom user
# by adding more required fields as declared below in the class
# like gender, country, currency, language, ets.,


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_HINDI = "hi"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_HINDI, "Hindi"))

    CURRENCY_USD = "usd"
    CURRENCY_INR = "inr"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_INR, "INR"))

    # null=True tells fatabase that null values can be accepted
    # blank=True means that filling the field is not compulsory

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_ENGLISH
    )

    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=3,
        blank=True,
        default=CURRENCY_INR,
    )

    superhost = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)

    email_secret = models.CharField(
        max_length=120,
        default="",
        blank=True,
    )

    def verify_email(self):
        # create a random secret key and send that to
        # the user email as link to get verified

        # id already verified, do nothing
        if self.email_verified is False:

            # generating a hex secret sreing for max length=20
            secret = uuid.uuid4().hex[:20]

            # getting email template from templates
            # and passing secret as context
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )

            self.email_secret = secret
            send_mail(
                "Account verification for Airbnb",
                "",
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
