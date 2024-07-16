from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from staff_manager.models import Position

admin.site.register(Position)


@admin.register(get_user_model())
class StaffAdmin(UserAdmin):
    list_display = [
        "username", "first_name", "last_name", "staff_position", "email"
    ]
    fieldsets = UserAdmin.fieldsets + (
        ("Positions", {"fields": ("position", )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Positions", {"fields": ("position", )}),
    )
    list_filter = ["position"]
    search_fields = ["first_name", "last_name", "username"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("position")

    def staff_position(self, obj):
        return ", ".join([pos.name for pos in obj.position.all()])
