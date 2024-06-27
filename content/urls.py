from django.urls import path

from .views import (
    index,
    ContentTypeListView,
    PositionListView,
    PositionDetailView,
    StaffListView,
    StaffDetailView,
    TaskListView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "content-types/",
        ContentTypeListView.as_view(),
        name="content-type-list"
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/<int:pk>",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]

app_name = "content"
