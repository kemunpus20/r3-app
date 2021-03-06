# R3
A simple web-based system for experimenting with how external image, video, and textual information enhances a person's creativity, based on the AUT ('Alternate Uses Task' Guilford,1967) theory of evaluation.

![screenshot](doc/screenshot.png)

## Getting started
- To host of experiment, Please read this document to develop and/or deploy this system in your own environment.
- Pull requests, feature ideas and bug reports are very welcome.

### System requirements
- Server : [Python](https://www.python.org/) 3.7 and [Django](https://www.djangoproject.com/) 3.0. Depended modulses are described in [requirements.txt](requirements.txt).
- Client : Modern browser that supports JavaScript and HTML5. Chrome, Firefox, and New Edge would be fine. I am very sorry that IE11 does not work correctly due to lack of CSS support.

### Install to your development environment
If you already had a development environment with Python 3, following steps (as like general Django application) will installs the system to your environment, and just starts it on 'Debug' mode.
```
$ pip instll -r requirements.txt
$ ./manage.py check
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver
```
Now you can acccess http://localhost:8000 to get application main screen and http://localhost:8000/manager to open Django built-in administration application with superuser regstered in above step. Be sure that path to administration screen has been changed from default value "admin" to "manahger" for security reason. And also you can use `gunicorn --bind=0.0.0.0:8000 pbl.wsgi` instead of `manage.py runserver` as similar to the production environment.

### Setup data for your test drive
To prepare minimam data, follow below steps in the administration application.
 1. Add your several media files (should be jpg or mp4) using "Media" menu.
 1. Create your own experiment logic using "Logic" menu.
 1. "Prep" your logic using "Prep selected logics" menu in the Logic list. This operation assigns relavant media files to the logic.
 1. Launch main application with http://localhost:8000 and try to start your experiment using the logic you created.

### Install to your production environment
 I have decided to use [Microsoft Azure](https://azure.microsoft.com) as my production environment. And the system will be deployed automatically when code has been comitted to this GutHub repository "main" branch. Regarding deployment to Azure, please read separated document [How to deploy to Azure](doc/PRODUCTION.md).

## Restrictions and known issues
1. This system does not provide any original media streaming / decoding mechanism, so supported media format is completely depends on the client browser and codecs. For example, legacy quicktime format which basically has .mov extention does not supported by latest browsers. Hence If you need to use your original good old family movie recorded by traditional digital camera, you may have to convert that to mp4. [FFmpeg](https://ffmpeg.org/) cound be a solution in the case.
1. Back-end media storage always accepts any data as a media file. But client-side javascript (see [play.html](r3/templates/play.html)) that handles media data is restricted to mp4, webm, jpg and png only.
1. Maximum size of media file should be less than 30M bytes, and maximum number of medias that can be assigned to one logic is 100. Modify [models.py](r3/models.py) if you have to change this limitation.
1. User can anytime use any browser buttons like a "back" and "reload". There is no impact to the system from data consistency point of view, but it might be confused from experiment participant point of view.
1. Experiment host has to update every Logics when new Media file has been added. At this stage, this process called "Prep" is implemented as a part of synchronous HTTP handler. So perhaps client browser will be timed-out in "Prep" process if bunch of media files registererd in the system. Data stored back-end will be updated successfully even if client is timed-out. So I think this is not a critical issue at the moment.

## References
Many thanks to all of authors.
 - [Django on Azure - beyond "hello world"](https://tonybaloney.github.io/posts/django-on-azure-beyond-hello-world.html)
 - [Tutorial: Deploy a Django web app with PostgreSQL using the Azure portal](https://docs.microsoft.com/ja-jp/azure/developer/python/tutorial-python-postgresql-app-portal)
 - [DjangoにPostgreSQLを適用する](https://qiita.com/shigechioyo/items/9b5a03ceead6e5ec87ec)
 
 ## Note
See my personal [note](doc/NOTE.md) if you are interested. 
