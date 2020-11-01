""" Logics """

import datetime
import json
import os
import random

from django.http import Http404

from .models import Media


def prep(logic):
    """
    実際のprep実装に処理を渡すためのインタフェースです.

    Parameters
    ----------
    logic : Logic
        準備(prep)をするlogicオブジェクト.
    """

    param_list = logic.param.split()

    # 結果のリストを空にしておきます.
    logic.media_list = ""
    logic.media_count = 0

    # 実装を呼び出します.
    if "default_logic" in param_list:
        default_prep(logic, param_list)

    elif "dynamic_logic" in param_list:
        dynamic_prep(logic, param_list)

    else:

        # 知らないLogicの名前が指定されたらエラーです.
        raise Http404

    # 結果を保存して終了です.
    logic.save()


def get_content(trial, seq):
    """
    実際のget_content実装に処理を渡すためのインタフェースです.

    Parameters
    ----------
    trial : Trial
        実行中のTrialオブジェクト.
    seq : int
         表示を要求されたMediaのシーケンス番号.
    """

    # Trialに結び付けられているLogicを取得します.
    logic = trial.logic

    # Logicのparamを取り出します.
    param_list = logic.param.split()

    # paramで指定されているget_contentを呼びだします.
    if "default_logic" in param_list:
        return default_get_content(trial, seq, param_list)

    elif "dynamic_logic" in param_list:
        return dynamic_get_content(trial, seq, param_list)

    else:
        raise Http404


def default_prep(logic, param_list):
    """
    もっとも基本的なlogicです.
    単純に条件に合致するMediaを検索してリストに保存します.
    """

    # 実行開始の情報をstateに書いておきます.
    state = str(datetime.datetime.today())
    state += " default_prep started."
    logic.state = state
    logic.save()

    # 対象となるMediaをすべて新しい順に取得します.
    media_all = Media.objects.all().order_by("updated").reverse()

    # 表示対象として指定されている拡張子のリストを取得します.
    ext_list = logic.media_ext.split()
    logic.media_ext = " ".join(map(str, ext_list))

    # 表示対象として指定されているタグのリストを取得します.
    tag_list = logic.media_tag.split()
    logic.media_tag = " ".join(map(str, tag_list))

    # 結果のMediaの主キーのリストを保持する空の配列を準備しておきます.
    media_list = []

    # すべてのMediaを順番に処理していきます.
    for media in media_all:

        # 拡張子の指定が*か、もしくは指定リストに含まれている?
        if ("*" in ext_list) or (media.ext in ext_list):
            matched = False

            if "*" in tag_list:

                # 対象となる拡張子が*で指定されているのならそのMediaは採用です.
                matched = True

            else:

                # それ以外の場合にはMediaの拡張子がリストに含まれているか確認します.
                media_tag_list = media.tag.split()

                if not set(media_tag_list).isdisjoint(tag_list):

                    # 含まれていればそのMediaは採用です.
                    matched = True

            if matched:

                # 採用の場合は結果リストに追記しておきます.
                media_list.append(media.id)

    # 採用されたMediaの個数を保管しておきます.
    logic.media_count = len(media_list)

    # Logicのparamにshuffleが指定されていれば結果のリストをシャッフルします.
    if "shuffle" in param_list:
        random.shuffle(media_list)

    # リストを空白区切りの文字列に展開します.
    # この辺は量が多くなった場合にはもう少し別の方法を考えるべきです...
    logic.media_list = " ".join(map(str, media_list))

    # 実行終了の情報をstateに書いておきます.
    state += os.linesep
    state += str(datetime.datetime.today())
    state += " default_prep finished."
    logic.state = state

    # データベースに結果を書き込んで終了です.
    logic.save()


def default_get_content(trial, seq, param_list):
    """
    もっとも基本的なlogicです.
    すでに単純に条件に合致するMediaを検索してリストに保存してありますので、そのseq番目を返します.
    """

    # 実行中のTrialに結び付けられているLogicを取得します.
    logic = trial.logic

    # そのLogicが持っているMediaのリストを取得します.
    media_list = logic.media_list.split()
    media_count = len(media_list)

    if media_count == 0:

        # 表示すべきデータが一個もない場合はエラーにはせずにメッセージを出すようにします.
        return json.dumps({"ext": "txt", "url": "No data to show"})

    else:

        # seq番目のMediaをとってきます.
        media_index = int(seq) % media_count
        media = Media.objects.get(pk=media_list[media_index])

        if media:

            # Mediaが無事に取れた場合にはjsonを返します.
            return json.dumps({"ext": media.ext, "url": media.content.url})

    # Mediaが見つからなかった場合は404を返します.
    raise Http404


def dynamic_prep(logic, param_list):
    """
    動的にMediaを取得するLogicです.まだ何も実装していません.
    """
    pass


def dynamic_get_content(trial, seq, param_list):
    """
    動的にMediaを取得するLogicです.まだ何も実装していません.
    """

    raise Http404
