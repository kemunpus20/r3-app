from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import FinishForm, MainForm, PlayhForm, StartForm
from .logics import get_content
from .models import Trial


class MainView(generic.CreateView):
    model = Trial
    template_name = "main.html"
    form_class = MainForm

    def get_success_url(self):
        return reverse("r3:start", kwargs={"pk": self.object.id})


class StartView(generic.UpdateView):
    model = Trial
    template_name = "start.html"
    form_class = StartForm

    def get_success_url(self):
        return reverse("r3:play", kwargs={"pk": self.object.id})


class PlayView(generic.UpdateView):
    model = Trial
    template_name = "play.html"
    form_class = PlayhForm

    def get_success_url(self):
        return reverse("r3:finish", kwargs={"pk": self.object.id})


class FinishView(generic.UpdateView):
    model = Trial
    template_name = "finish.html"
    form_class = FinishForm

    def get_success_url(self):
        return reverse_lazy("r3:main")


def content_handler(request, pk, seq):
    trial = Trial.objects.get(pk=pk)

    if trial:
        return HttpResponse(get_content(trial, seq), content_type="application/json")

    raise Http404
