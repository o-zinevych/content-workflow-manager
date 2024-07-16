from django.urls import path

from .views import (
    IndexView,
    ContentTypeListView,
    ContentTypeCreateView,
    ContentTypeUpdateView,
    ContentTypeDeleteView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    UpdateTaskStaffView,
    TaskDeleteView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
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
    path(
        "content-types/<int:pk>/delete/",
        ContentTypeDeleteView.as_view(),
        name="content-type-delete"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/update-staff/",
        UpdateTaskStaffView.as_view(),
        name="task-staff-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
]

app_name = "content"
