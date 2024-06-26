from django.urls import path

from .views import (
    index,
    ContentTypeListView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "content-types/",
        ContentTypeListView.as_view(),
        name="content-type-list"
    ),
]

app_name = "content"
