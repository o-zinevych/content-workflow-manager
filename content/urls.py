from django.urls import path

from .views import (
    index,
    ContentTypeListView,
    ContentTypeCreateView,
    PositionListView,
    PositionDetailView,
    PositionCreateView,
    StaffListView,
    StaffDetailView,
    StaffCreateView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "content-types/",
        ContentTypeListView.as_view(),
        name="content-type-list"
    ),
    path(
        "content-types/create/",
        ContentTypeCreateView.as_view(),
        name="content-type-create"
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("staff/create/", StaffCreateView.as_view(), name="staff-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
]

app_name = "content"
