from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.http import Http404
from django_countries import Countries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from . import models
from . import forms

# Create your views here.
# this function is no longer required, just kept for reference
def all_rooms(request):

    # if the request obj contains a page query get it else defaults to 1
    page = request.GET.get("page", 1)
    # get reference to all room objects in database
    room_list = models.Room.objects.all()
    # creates a django paginator object for high pagination simplification
    paginator = Paginator(room_list, 10, orphans=5)
    # orphans=5 means if there are 5 items or less in last page
    # it will be sent along in the second last page

    """one page object contains a query set of the required rooms in object_list
    as well as several other details such as count for total objects,
    num_pages for total pages
    per_page for um of items per page"""

    """paginator.get_page does all error handling on its own
    whereas paginator.page enables more customization
    by allowing us to handle errors on our own"""

    # rooms = paginator.get_page(page)
    # print(dir(rooms.paginator))

    # the rooms varialble includes rooms.paginator as well
    # which contains more details

    try:
        rooms = paginator.page(page)
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")
    except PageNotAnInteger:
        return redirect("/")
    except InvalidPage:
        return redirect("/")


# class based views helps reduce boilerplate code even more
# the code above and below do same thing

# function based views as above in general offer more customizability
class HomeView(ListView):

    """ Homeview Model """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    # like /page=2, /page-3.... we can make like /potato=2, or /potato=3
    # basically name of this query argument
    page_kwarg = "page"

    # in the html of this class we will use for room in rooms
    # instead of the default object_list
    context_object_name = "rooms"

    # to add custom data to the view
    """ def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        # sending additional key value pairs to the view i.e. room_list.html
        context["now"] = now
        return context """


# a function based view for room detail
# we will also create a class based view below


# the pk argument passed in rooms.urls will be here
def room_detail(request, pk):

    # if the pk in url is something that is not in the database
    # an exception will occur which has to be caught
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
    # create a "404.html" file to display that particular page
    # return redirect(reverse("core:home"))
    #  or we can do redirect("/") but above keeps professional

    # print(vars(room))


# in urls it is called as views.RoomDetail.as_view()
# unlike function based views which are just called
# as views.function_name


""" but how does django know that we are passing a primary key in the url
 in Detailview, django by default looks for a pk argument 
 you can also tell on your own how 'pk' (<int:pk>) looks in the url 
 by calling pk_url_kwarg="potato" if url contains <int:potato> """


# also you don't have to explicitly catch exceptions here
# for a page not found, it will automatically throw a 404 error


class RoomDetail(DetailView):

    """ Room Detail Definition"""

    # this is required otherwise Improperly Configured error is thrown
    model = models.Room

    # if html tmeplate not found it will give this error
    # TemplateDoesNotExist at /rooms/178
    # rooms/room_detail.html
    """ FYI the template name is decided by model name
    here Room and the class it inherits here DetailView
    hence template name should be room_detail.html"""


def search(request):

    # the form will forget data next time it reloads
    # form = forms.SearchForm()

    # now it will remember
    country = request.GET.get("country")
    if country:
        form = forms.SearchForm(request.GET)
        # this is a bounded request, this had to be done otherwise
        # it will show us country field is required
        if form.is_valid():
            print("cleaned form data= ", form.cleaned_data)
            # cleaned data will allow us to return the response to the qureies
            # here, rooms matching the filter requirements
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

        # if there is a city query, i.e., it is not anywhere
        # then we filter the rooms with city starts with the city entered
        if city != "Anywhere":
            filter_args["city__startswith"] = city

        # there is no condition for country since the defaunt is India
        # hence, we filter rooms by country same as entered country
        filter_args["country"] = country

        # condition where no room type is chosen
        # otherwise we filter rooms which have roomtype pk as the entered roomtype pk
        if room_type is not None:
            filter_args["room_type"] = room_type

        # filtering by price
        # if user has filtered by price return all rooms with price
        # less than or equal to that price (lte)
        if price is not None:
            filter_args["price__lte"] = price

        if guests is not None:
            filter_args["guests__gte"] = guests

        if bedrooms is not None:
            filter_args["bedrooms__gte"] = bedrooms

        if beds is not None:
            filter_args["beds__gte"] = beds

        if baths is not None:
            filter_args["baths__gte"] = baths

        if instant_book is True:
            filter_args["instant_book"] = True

        if superhost is True:
            filter_args["host__superhost"] = True

        # filter by amenities
        # because we have a query set of amenities
        # we need to filter by each of them
        for amenity in amenities:
            filter_args["amenities"] = amenity

        # filter by facilities
        # same as above
        for facility in facilities:
            filter_args["facilities"] = facility

        print("entered filter arguments= ", filter_args)
        querySet = models.Room.objects.filter(**filter_args).order_by("-created")
        print("entire query set=", querySet)

        paginator = Paginator(querySet, 10, orphans=5)
        page = request.GET.get("page", 1)

        rooms = paginator.get_page(page)
        print("current page", type(page), page)
        print("current rooms= ", dir(rooms), rooms)
        print(rooms.object_list)
        print(rooms.end_index)
        print(rooms.has_next)
        print(rooms.has_other_pages)
        print(rooms.has_previous)
        print(vars(rooms.paginator))
        print(rooms.number)

        return render(request, "rooms/search.html", {"form": form, "rooms": rooms})

    else:
        form = forms.SearchForm()
        # unbounded request

    return render(request, "rooms/search.html", {"form": form})


# DJANGO forms API (above) helps us achive everything below
"""def search(request):
    # print(request)
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "IN")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    baths = int(request.GET.get("baths", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    print(s_amenities, s_facilities)

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    form_fields = {
        "countries": Countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    request_fields = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "baths": baths,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    to filter and get results we could do models.Room.objects.filter(clause)
    and filter and filter again and again depending upon te query parameters 
    checkout Querysets field lookups for documentation  
    https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4

    # or we could do as below

    filter_args = {}

    # if there is a city query, i.e., it is not anywhere
    # then we filter the rooms with city starts with the city entered
    if city != "Anywhere":
        filter_args["city__startswith"] = city

    # there is no condition for country since the defaunt is India
    # hence, we filter rooms by country same as entered country
    filter_args["country"] = country

    # condition where no room type is chosen
    # otherwise we filter rooms which have roomtype pk as the entered roomtype pk
    # if room_type != 0:
    #     filter_args["room_type__pk"] = room_type

    # filtering by price
    # if user has filtered by price return all rooms with price
    # less than or equal to that price (lte)
    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    # filter by amenities
    # because we have an array of amenities
    # we need to filter by each of them
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    # filter by facilities
    # same as above
    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    print(filter_args)
    rooms = models.Room.objects.filter(**filter_args)

    print(rooms)
    print(models.RoomType.objects.get(pk=room_type))

    return render(
        request,
        "rooms/search.html",
        {**form_fields, **request_fields, "rooms": rooms},
    )"""
