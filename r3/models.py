""" Models """

import uuid

from django.core.exceptions import ValidationError
from django.db import models

FILE_SIZE_LIMIT = 30 * 1024 * 1024


def generate_filename(_, filename):
    return "%s.%s" % (uuid.uuid4(), filename.split(".")[-1].lower())


def filesize_validator(file):

    if file.size > FILE_SIZE_LIMIT:

        raise ValidationError(
            "File too large. Size should not exceed {} MB.".format(
                FILE_SIZE_LIMIT / (1024 * 1024)
            )
        )


class Media(models.Model):
    updated = models.DateTimeField(auto_now=True)
    content = models.FileField(
        blank=False, upload_to=generate_filename, validators=[filesize_validator]
    )
    ext = models.CharField(blank=False, max_length=10)
    source = models.CharField(blank=False, max_length=100)
    tag = models.CharField(blank=True, max_length=1000)


class Logic(models.Model):
    name = models.CharField(blank=False, max_length=50)
    param = models.CharField(blank=False, default="default_logic", max_length=100)
    start_prompt = models.TextField(blank=True, max_length=1000)
    finish_prompt = models.TextField(blank=True, max_length=1000)
    interval = models.IntegerField(default=5)
    media_ext = models.CharField(blank=False, default="*", max_length=50)
    media_tag = models.CharField(blank=False, default="*", max_length=1000)
    media_list = models.CharField(blank=True, max_length=8000)
    media_count = models.IntegerField(default=0)
    state = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return str(self.name)


class Trial(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)
    room = models.CharField(blank=False, max_length=20)
    logic = models.ForeignKey("Logic", on_delete=models.PROTECT)
    nickname = models.CharField(blank=True, max_length=20)
    keyword = models.CharField(blank=True, max_length=1000)
    comment = models.TextField(blank=True, max_length=1000)
