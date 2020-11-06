""" Models """

import uuid

from django.core.exceptions import ValidationError
from django.db import models

MAX_MEDIA_COUNT = 100

MEDIA_LIST_SIZE = len("2147483647 ") * MAX_MEDIA_COUNT

MEDIA_FILE_SIZE_LIMIT = 30 * (1024 * 1024)


def media_filename(_, filename):
    return "{}.{}".format(uuid.uuid4(), filename.split(".")[-1].lower())


def media_validator(file):

    if file.size > MEDIA_FILE_SIZE_LIMIT:

        raise ValidationError(
            "File too large. Size should not exceed {} MB.".format(
                MEDIA_FILE_SIZE_LIMIT / (1024 * 1024)
            )
        )


class Media(models.Model):
    updated = models.DateTimeField(auto_now=True)
    content = models.FileField(
        blank=False, upload_to=media_filename, validators=[media_validator]
    )
    ext = models.CharField(blank=False, max_length=10)
    source = models.CharField(blank=False, max_length=100)
    tag = models.CharField(blank=True, max_length=1000)


class Logic(models.Model):
    name = models.CharField(blank=False, max_length=50)
    param = models.CharField(
        blank=False, default="logic=media shuffle", max_length=1000
    )
    note = models.TextField(blank=True, max_length=1000)
    start_prompt = models.TextField(blank=True, max_length=1000)
    finish_prompt = models.TextField(blank=True, max_length=1000)
    interval = models.IntegerField(blank=False, default=5)
    media_ext = models.CharField(blank=False, default="*", max_length=50)
    media_tag = models.CharField(blank=False, default="*", max_length=1000)
    media_list = models.CharField(blank=True, max_length=MEDIA_LIST_SIZE)
    media_count = models.IntegerField(blank=False, default=0)
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
