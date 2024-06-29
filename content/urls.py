from django.urls import path

from .views import (
    index,
    ContentTypeListView,
    ContentTypeCreateView,
    ContentTypeUpdateView,
    PositionListView,
    PositionDetailView,
    PositionCreateView,
    PositionUpdateView,
    StaffListView,
    StaffDetailView,
    StaffCreateView,
    StaffUpdateView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
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
    path(
        "content-types/<int:pk>/update/",
        ContentTypeUpdateView.as_view(),
        name="content-type-update"
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
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("staff/create/", StaffCreateView.as_view(), name="staff-create"),
    path(
        "staff/<int:pk>/update/",
        StaffUpdateView.as_view(),
        name="staff-update",
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
]

app_name = "content"
