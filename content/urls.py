from django.urls import path

from .views import (
    index,
    ContentTypeListView,
    PositionListView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "content-types/",
        ContentTypeListView.as_view(),
        name="content-type-list"
    ),
    path("positions/", PositionListView.as_view(), name="position-list")
]

app_name = "content"
