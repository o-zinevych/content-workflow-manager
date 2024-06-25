from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from content.models import ContentType, Position, Staff, Task

admin.site.register(ContentType)
admin.site.register(Position)


@admin.register(Staff)
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


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "priority",
        "is_finished",
        "content_type",
        "staff_involved"
    ]
    list_filter = ["priority", "is_finished", "content_type", "staff"]
    search_fields = ["name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return (queryset.select_related("content_type")
                .prefetch_related("staff"))

    def staff_involved(self, obj):
        return ", ".join([staff.username for staff in obj.staff.all()])
