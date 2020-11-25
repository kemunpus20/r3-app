import django
from django.contrib import admin, messages
from import_export import resources
from import_export.admin import ExportActionMixin, ExportMixin
from import_export.formats import base_formats

from .logics import prep
from .models import Logic, Media, Temp, Trial

admin.site.unregister(django.contrib.auth.models.User)
admin.site.unregister(django.contrib.auth.models.Group)


@admin.register(Logic)
class LogicAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "name", "subject", "media_count")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    actions = ["prep_selected_logics"]
    list_per_page = 10

    def prep_selected_logics(self, request, queryset):

        for logic in queryset:
            prep(logic)

        messages.info(request, "'Prep' successfully done.")


@admin.register(Media)
class MediaAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "updated", "ext", "content", "source", "tag")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    exclude = ("ext",)
    list_per_page = 10

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
            "comment",
        )


@admin.register(Trial)
class TrialAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("id", "started", "room", "nickname", "logic")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    actions = ["merge_selected_trials"]
    list_per_page = 10
    resource_class = TrialResource

    def merge_selected_trials(self, request, queryset):
        TEMP_NAME = "merged trials"
        temp = Temp.objects.create()
        temp.name = TEMP_NAME
        data = '"Room","Nickname","Logic","Duration","Comment"'
        data += "\n"

        for trial in queryset:
            comment = trial.comment

            if len(comment) == 0:
                comment = "<empty>"

            comment_list = comment.splitlines()

            for comment_line in comment_list:

                if len(comment_line) > 0:
                    data += '"{}","{}","{}","{}","{}"'.format(
                        trial.room,
                        trial.nickname,
                        trial.logic.name,
                        trial.logic.duration,
                        comment_line,
                    )
                    data += "\n"

        temp.content = data
        temp.save()

        messages.info(
            request,
            "'Merge' successfully done. see latest data named '{}' in 'Temps' Table.".format(
                TEMP_NAME
            ),
        )


@admin.register(Temp)
class TempAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("id", "updated", "name")
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.HTML]
    list_per_page = 10
