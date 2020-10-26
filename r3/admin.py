""" Admin """

import django
from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export.formats import base_formats

from .logics import prep
from .models import Logic, Media, Trial

admin.site.unregister(django.contrib.auth.models.User)
admin.site.unregister(django.contrib.auth.models.Group)


@admin.register(Logic)
class LogicAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "param", "media_count")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    actions = ["prep_selected_logics"]

    def prep_selected_logics(self, _, queryset):

        for logic in queryset:
            prep(logic)


@admin.register(Media)
class MediaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "updated", "ext", "content", "source", "tag")
    exclude = ("ext",)
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]

    def save_model(self, request, obj, form, change):
        obj.ext = str(obj.content).split(".")[-1].lower()
        obj.save()


class TrialResource(resources.ModelResource):
    class Meta:
        model = Trial
        fields = (
            "id",
            "started",
            "finished",
            "room",
            "nickname",
            "logic__name",
            "keyword",
            "comment",
        )


@admin.register(Trial)
class TrialAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "started", "finished", "room", "nickname", "logic")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    resource_class = TrialResource
