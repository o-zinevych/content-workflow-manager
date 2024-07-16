from django.contrib import admin

from content.models import ContentType, Task

admin.site.register(ContentType)


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
