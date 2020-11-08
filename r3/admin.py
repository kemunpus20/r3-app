""" Admin """

import django
from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ExportActionMixin, ExportMixin
from import_export.formats import base_formats

from .logics import prep
from .models import Logic, Media, Trial, Work, Temp

admin.site.unregister(django.contrib.auth.models.User)
admin.site.unregister(django.contrib.auth.models.Group)


@admin.register(Logic)
class LogicAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "name", "param", "media_count")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    actions = ["prep_selected_logics"]

    def prep_selected_logics(self, request, queryset):

        for logic in queryset:
            prep(logic)

        messages.info(request, "'Prep' successfully done.")


@admin.register(Media)
class MediaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "updated", "ext", "content", "source", "tag")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    exclude = ("ext",)

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
class TrialAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "started", "finished", "room", "nickname", "logic")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    actions = ["merge_selected_trials"]
    resource_class = TrialResource

    def merge_selected_trials(self, request, queryset):
        WORK_NAME = "merged trials"
        work = Work.objects.create()
        work.name = WORK_NAME
        data = '"Room","Nickname","Logic.note","Logic.name","Logic.duration","Comment"'
        data += "\n"

        for trial in queryset:
            comment = trial.comment

            if len(comment) == 0:
                comment = "NO-COMMENT"

            comment_list = comment.split()

            for c in comment_list:
                data += '"{}","{}","{}","{}","{}","{}"'.format(
                    trial.room,
                    trial.nickname,
                    trial.logic.note,
                    trial.logic.name,
                    trial.logic.duration,
                    c,
                )
                data += "\n"

        work.content = data
        work.save()

        messages.info(
            request,
            "'Merge' successfully done. see latest data named '{}' in 'Works' Table.".format(
                WORK_NAME
            ),
        )


@admin.register(Work)
class WorkAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "updated", "name")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]


@admin.register(Temp)
class TempAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "updated", "name")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
