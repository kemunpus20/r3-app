# MEMO
たんなる自分用のメモです。

##  いろいろ
 1. pipでインストールしたもの: django, django-import-export, django-cleanup, whitenoise, django-pyodbc-azure, black, flake8
 1. ユーザでインストールしたので.profileで.local/binをPATHに追加
 1. pip list --outdated で古くなっちゃったのが確認できる
 1. black, flake8, isort はそれぞれ独立して実行可能
 1. gnucorn の起動 : gunicorn3 --bind 127.0.0.1:8000 pbl.wsgi


## PostgreSQL
 - sudo -u postgres psql
 - CREATE DATABASE r3;
 - CREATE USER PSQLADMIN WITH PASSWORD 'PASSWORD';
 - ALTER ROLE PSQLADMIN SET client_encoding TO 'utf8';
 - ALTER ROLE PSQLADMIN SET default_transaction_isolation TO 'read committed';
 - ALTER ROLE PSQLADMIN SET timezone TO 'Asia/Tokyo';
 - GRANT ALL PRIVILEGES ON DATABASE r3 TO PSQLADMIN;
 - /q

## Azure
 1. Guthubからデプロイ設定したあと、sshで入って pip install -r requirements.txt, manage.py createsuperuserする

## わかっている制限
 1. 静止画はjpg,png 動画はmp4,webm,oggだけのサポート(それ以外のファイルも登録はできるけどあえて再生時に処理しないようにしている)
 1. ローカルで動くツールでサポートしていた「単語」の表示機能は今のところない
 1. ブラウザはHTML5のモダンブラウザでJavaScriptが有効になっていないとだめ

## 本番化にむけて
 1. STATICファイルの扱いを確認
 1. SECRET_KEYの処理,manage.pyでのセキュリティチェックを実施する
 1. 緊急用のユーザとチームメンバー公開用のユーザの２つを作成する
 1. DBのバックアップとリストアを用意する
 
## つぎにやる
 1. READMEとかもうちょっと書く
 1. Loggerをもうちょっとつける
 1. Logicにコメントをつける
 1. ログがうざいのでfaviconつける?
 1. Logic.dynamicなんちゃらをつくる(Trial.keywordを使ってなにかする)
 1. Testをつける
 1. RemoteRandomViewerをリポジトリにいれて整理する

## いつかやる
 1. 自動Prep機能?
 1. モバイルブラウザ対応,SPA対応とか?
 