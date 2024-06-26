from django.urls import path

from .views import (
    index,
    ContentTypeListView,
    PositionListView,
    StaffListView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "content-types/",
        ContentTypeListView.as_view(),
        name="content-type-list"
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("staff/", StaffListView.as_view(), name="staff-list")
]

app_name = "content"
