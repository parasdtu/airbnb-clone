from django import forms
from django_countries.fields import CountryField
from . import models

# it also allows us to change/ customise widgets of the fields
# like CharField uses a Textfield but we can make it use textEdit field

# similarly ModelMultiplehoiceField used a dropdown
# but we make it use a check box list


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="IN").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)

    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    # queryset is important for it to generate fields
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
