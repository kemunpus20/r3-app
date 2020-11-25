from django.urls import path

from . import views

app_name = "r3"

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("start/<int:pk>", views.StartView.as_view(), name="start"),
    path("play/<int:pk>", views.PlayView.as_view(), name="play"),
    path("finish/<int:pk>", views.FinishView.as_view(), name="finish"),
    path("content/<int:pk>/<int:seq>", views.content_handler, name="content"),
]
