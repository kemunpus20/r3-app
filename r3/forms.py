""" Forms """

from django import forms

from .models import Trial


class MainForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ("room", "nickname", "logic", "keyword")

    def clean_room(self):
        room = str(self.cleaned_data.get("room")).strip()

        if len(room) < 6 or room[0:1] != "3":
            raise forms.ValidationError("Please ask to the team member.")

        return room


class FinishForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ("comment",)
