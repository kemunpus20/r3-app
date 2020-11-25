""" Logics """

import datetime
import json
import random

from django.http import Http404

from .models import MAX_MEDIA_COUNT, Media, Temp


def add_state(logic, message):
    logic.state += "{} {}\n".format(str(datetime.datetime.today()), message)


def prep(logic):
    logic.media_list = ""
    logic.media_count = 0
    logic.state = ""

    add_state(logic, logic.implement + " prep started")
    logic.save()

    if logic.implement == "media":
        media_prep(logic)

    elif logic.implement == "text":
        text_prep(logic)

    elif logic.implement == "blank":
        blank_prep(logic)

    else:
        add_state(logic, "unknown logic " + logic.implement)
        raise Http404

    add_state(logic, logic.implement + " prep finished")
    logic.save()


def get_content(trial, seq):
    logic = trial.logic

    if logic.implement == "media":
        return media_get_content(trial, seq)

    elif logic.implement == "text":
        return text_get_content(trial, seq)

    elif logic.implement == "blank":
        return blank_get_content(trial, seq)

    raise Http404


def media_prep(logic):
    ext_list = logic.media_ext.split()
    logic.media_ext = " ".join(map(str, ext_list))

    tag_list = logic.media_tag.split()
    logic.media_tag = " ".join(map(str, tag_list))

    media_list = []
    media_all = Media.objects.all().order_by("id").reverse()

    for media in media_all:

        if media.ext == "txt":
            continue

        if ("*" in ext_list) or (media.ext in ext_list):
            matched = False

            if "*" in tag_list:
                matched = True

            else:
                media_tag_list = media.tag.split()

                if not set(media_tag_list).isdisjoint(tag_list):
                    matched = True

            if matched:

                if len(media_list) >= MAX_MEDIA_COUNT:
                    break

                media_list.append(media.id)

    if logic.media_order == "shuffle":
        random.shuffle(media_list)

    media_list_str = " ".join(map(str, media_list))
    logic.media_list = media_list_str
    logic.media_count = len(media_list)


def media_get_content(trial, seq):
    logic = trial.logic

    media_list = logic.media_list.split()
    media_count = len(media_list)

    if media_count == 0:
        return json.dumps({"type": "txt", "data": "No data to show"})

    media_index = int(seq) % media_count
    media = Media.objects.get(pk=media_list[media_index])

    if media:
        return json.dumps({"type": media.ext, "data": media.content.url})

    raise Http404


TEXT_LOGIC_NAME = "text-logic-cache:{}"


def text_prep(logic):
    text_list = []
    tag_list = logic.media_tag.split()
    logic.media_tag = " ".join(map(str, tag_list))
    media_all = Media.objects.all()

    for media in media_all:

        if media.ext == "txt":
            media_tag_list = media.tag.split()

            if not set(media_tag_list).isdisjoint(tag_list):

                with media.content.open(mode="rb") as text_file:
                    lines = text_file.read().decode("utf-8").splitlines()
                    text_file.close()
                    text_list.extend(lines)

    index_list = list(range(len(text_list)))

    if logic.media_order == "shuffle":
        random.shuffle(index_list)

    max_index = min(len(index_list), MAX_MEDIA_COUNT)
    media_list_str = " ".join(map(str, index_list[:max_index]))

    logic.media_list = media_list_str
    logic.media_count = max_index

    name = TEXT_LOGIC_NAME.format(logic.pk)
    temp = None

    try:
        temp = Temp.objects.get(name=name)

    except Temp.DoesNotExist:
        temp = Temp.objects.create()
        temp.name = name

    temp.content = " ".join(map(str, text_list))
    temp.save()


def text_get_content(trial, seq):
    logic = trial.logic

    index_list = logic.media_list.split()
    index_count = len(index_list)

    if index_count == 0:
        return json.dumps({"type": "txt", "data": "No data to show"})

    name = TEXT_LOGIC_NAME.format(logic.pk)
    temp = Temp.objects.get(name=name)
    text_list = temp.content.split()

    text = text_list[int(index_list[int(seq) % index_count])]

    return json.dumps({"type": "txt", "data": text})


def blank_prep(logic):
    pass


def blank_get_content(trial, seq):
    return json.dumps({"type": "txt", "data": ""})
