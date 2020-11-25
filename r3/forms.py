import random

from django import forms

from .models import Trial


class MainForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ("room", "nickname", "logic")

    def clean_room(self):
        room = str(self.cleaned_data.get("room")).strip()

        if len(room) < 6 or room[0:1] != "3":
            raise forms.ValidationError("Please ask to the team member.")

        return room

    def clean_nickname(self):
        nickname = str(self.cleaned_data.get("nickname")).strip()

        if len(nickname) == 0:
            # Gennerating anonymous name. use uuid instead if you need a perfect solution.
            nickname = "anonymous-" + str(random.randint(10000, 99999))

        return nickname


class StartForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ("comment",)


class PlayhForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ("comment",)


class FinishForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ("comment",)
