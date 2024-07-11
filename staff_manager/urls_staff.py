from django.urls import path

from .views import (
    StaffListView,
    StaffDetailView,
    StaffCreateView,
    StaffUpdateView,
    StaffDeleteView,
)

urlpatterns = [
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("staff/create/", StaffCreateView.as_view(), name="staff-create"),
    path(
        "staff/<int:pk>/update/",
        StaffUpdateView.as_view(),
        name="staff-update",
    ),
    path(
        "staff/<int:pk>/delete/",
        StaffDeleteView.as_view(),
        name="staff-delete",
    ),
]

app_name = "staff"
