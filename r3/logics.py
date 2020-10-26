""" Logics """

import json
import logging
import random

from django.http import Http404

from .models import Media

logger = logging.getLogger("django")

# Interfaces


def prep(logic):
    param_list = logic.param.split()

    logic.media_list = ""
    logic.media_count = 0

    if "default_logic" in param_list:
        default_prep(logic, param_list)

    elif "dynamic_logic" in param_list:
        dynamic_prep(logic, param_list)

    else:
        raise Http404

    logic.save()


def get_content(trial, seq):
    logic = trial.logic
    param_list = logic.param.split()

    if "default_logic" in param_list:
        return default_get_content(trial, seq, param_list)

    elif "dynamic_logic" in param_list:
        return dynamic_get_content(trial, seq, param_list)

    else:
        raise Http404


# "Default Logic"


def default_prep(logic, param_list):
    logger.info("default_prep [{}].".format(logic.name))

    media_all = Media.objects.all().order_by("updated").reverse()

    ext_list = logic.media_ext.split()
    logic.media_ext = " ".join(map(str, ext_list))

    tag_list = logic.media_tag.split()
    logic.media_tag = " ".join(map(str, tag_list))

    media_list = []

    for media in media_all:

        if ("*" in ext_list) or (media.ext in ext_list):
            matched = False

            if "*" in tag_list:
                matched = True

            else:
                media_tag_list = media.tag.split()

                if not set(media_tag_list).isdisjoint(tag_list):
                    matched = True

            if matched:
                media_list.append(media.id)

    logic.media_count = len(media_list)

    if "shuffle" in param_list:
        random.shuffle(media_list)

    logic.media_list = " ".join(map(str, media_list))


def default_get_content(trial, seq, param_list):
    logic = trial.logic

    media_list = logic.media_list.split()
    media_count = len(media_list)

    if media_count > 0:
        media_index = int(seq) % media_count
        media = Media.objects.get(pk=media_list[media_index])

        if media:
            return json.dumps(
                {"ext": media.ext, "url": media.content.url}, ensure_ascii=False
            )

    raise Http404


# "Dynamic Logic (under construction)"


def dynamic_prep(logic, param_list):
    logger.info("dynamic_prep [{}].".format(logic.name))


def dynamic_get_content(trial, seq, param_list):
    raise Http404
