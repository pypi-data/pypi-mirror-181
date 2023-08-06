from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from tms_django_log import models


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("message", "level", "last_seen", "count")
    search_fields = ("message", "detail")
    list_per_page = 500
    actions = ["remove_all_logs"]
    ordering = ["-count"]

    @admin.action(description=_("Delete all logs"))
    def remove_all_logs(self, request, queryset):
        models.Log.objects.all().delete()
