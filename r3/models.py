""" Models """

import uuid

from django.core.exceptions import ValidationError
from django.db import models

MAX_MEDIA_COUNT = 100

MAX_MEDIA_LIST_SIZE = len("2147483647 ") * MAX_MEDIA_COUNT

MAX_MEDIA_FILE_SIZE_LIMIT = 30 * (1024 * 1024)

MAX_TEMP_CONTENT_SIZE = 1024 * 1


def media_filename(_, filename):
    return "{}.{}".format(uuid.uuid4(), filename.split(".")[-1].lower())


def media_validator(file):

    if file.size > MAX_MEDIA_FILE_SIZE_LIMIT:

        raise ValidationError(
            "File too large. Size should not exceed {} MB.".format(
                MAX_MEDIA_FILE_SIZE_LIMIT / (1024 * 1024)
            )
        )


class Media(models.Model):
    updated = models.DateTimeField(auto_now=True)

    content = models.FileField(
        blank=False,
        upload_to=media_filename,
        validators=[media_validator],
        help_text="Select data file to register as media data.",
    )

    ext = models.CharField(blank=False, max_length=10)

    source = models.CharField(
        blank=False,
        max_length=100,
        help_text="Specify owner and/or source information like URL.",
    )

    tag = models.CharField(
        blank=True,
        max_length=1000,
        help_text="Add some content-related tags separated by single space.",
    )


IMPLEMENT_CHOICES = {
    ("blank", "Blank : Nothing to show"),
    ("text", "Text : keyword"),
    ("media", "Media : Image and/or Video"),
}

ORDER_CHOICES = {
    ("shuffle", "Shuffle : Randomly"),
    ("id", "Id : By system generated ID"),
}

COMMENTING_CHOICES = {
    ("parallel", "Parallel : Enter simultaneously"),
    ("last", "Last : Enter at last of session"),
}


class Logic(models.Model):
    name = models.CharField(
        blank=False,
        max_length=50,
        help_text="Name that participants select at starts, sorted automatically.",
    )

    subject = models.CharField(
        blank=True,
        max_length=100,
        help_text="Brief description of this experiment that shows during the session.",
    )

    start_prompt = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Message to participants to show subject and goal of the experiment, use HTML tag if needed.",
    )

    finish_prompt = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Message to participants when the experiment finished, use HTML tag if needed.",
    )

    interval = models.IntegerField(
        blank=False,
        default=5,
        help_text="Interval time to switch presented media data, in seconds.",
    )

    duration = models.IntegerField(
        blank=False,
        default=30,
        help_text="Duration time of experiment, in seconds. zero means participants should finished manually.",
    )

    implement = models.CharField(
        blank=False,
        max_length=10,
        choices=IMPLEMENT_CHOICES,
        default="media",
        help_text="Algorithm that controls media data to show to participants.",
    )

    param = models.CharField(
        blank=True,
        max_length=1000,
        default="",
        help_text="Optional data that depends on each implementation.",
    )

    order = models.CharField(
        blank=False,
        max_length=10,
        choices=ORDER_CHOICES,
        default="shuffle",
        help_text="Displaying order of media data participants see.",
    )

    commenting = models.CharField(
        blank=False,
        max_length=10,
        choices=COMMENTING_CHOICES,
        default="parallel",
        help_text="Controls when participants enter comments as ideas.",
    )

    media_ext = models.CharField(
        blank=False,
        default="*",
        max_length=50,
        help_text="File extensions of media data that to show, separated by single space. '*' means everything.",
    )

    media_tag = models.CharField(
        blank=False,
        default="*",
        max_length=1000,
        help_text="Tag of media data that to show, separated by single space. '*' means everything.",
    )

    media_list = models.CharField(
        blank=True,
        max_length=MAX_MEDIA_LIST_SIZE,
        help_text="Do not edit directly - List of media IDs that created by 'prep' operation.",
    )

    media_count = models.IntegerField(
        blank=True,
        default=0,
        help_text="Do not edit directly - Count of media IDs that created by 'prep' operation.",
    )

    state = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Do not edit directly - Processing log data that created by 'prep' operation.",
    )

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


class Temp(models.Model):
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(blank=False, max_length=20)

    content = models.TextField(blank=True, max_length=MAX_TEMP_CONTENT_SIZE)
