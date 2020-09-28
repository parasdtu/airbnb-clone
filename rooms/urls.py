from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.search, name="search"),
]

# django allows variables in url paths
# hence int:pk is where the id of the room will go for room details
