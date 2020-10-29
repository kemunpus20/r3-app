# R3
Simple web-based system to support various internal hypothetical-based experiments to improve people's creativity.

## Getting started.
- To participant - Read the [tutorial](static/tutorial.html) (sorry in Japanese) on application main screen to join the experiment.
- To host of the experiment - Read this document to develop and/or deploy this system in your own environment.

## System requirements.
- Server-side : [Python](https://www.python.org/)3.7 and [Django](https://www.djangoproject.com/) 3.1 are key components of this system. I believe  this pair are most effective and productive platform for this kind of internal system. Depended modulses are described in [requirements.txt](requirements.txt).
- Client-side : Modern browser that supports JavaScript and HTML5. Chrome, Firefox, and New Edge would be fine. I am very sorry that IE11 does not work correctly due to lack of CSS support.

## Restrictions and know issues.
1. This system does not provide any additional media streaming / decoding mechanism, so supported media format is completely depends on the client browser and codecs. For example, legacy quicktime format which basically has .mov extention does not support in latest browsers anymore. Hence If you need to use your original good old family movie recorded by traditional digital camera, you may have to convert that to mp4. The [ffmpeg](https://ffmpeg.org/) cound be a solution in the case.
1. Back-end media storage always accept any data as a media file. But client-side javascript (see [play.html](r3/templates/play.html)) that handles media data is restricted to only for mp4, ogg, webm, jpg, or png.
1. Max size of media file should be less than 30M bytes. Modify [models.py](r3.models.py) if you have to change this limitation.
1. User can use any browser feature like a "back" and "reload" button. There is no impact to the system from data consistency point of view, but be sure this behavior from experiment participant point of view.
1. Since "prep" has been implemented as a part of synchronous HTTP handler, perhaps client browser will be timed-out in "prep" process if bunch of media files registererd in the system. Data stored back-end will be updated successfully even if client is timed-out. So I think this is not a critical issue at the moment.
1. Feature to showing some keywords as a hint instead of image or movie is not implemented yet. Please concider to use a script-based tool [RandomViwer.html](local_tool/RandomViewer.html) in that scenario.

## Install to your development environment.
If you already had a development environment with Python 3, following steps (as like an another Django  application) will installs the system to your environment, and just starts it as the 'Debug' mode.
```
$ pip instll -r requirements.txt
$ ./manage.py check
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```
Now you can acccess http://localhost:8000 to get the main screen and http://localhost:8000/manager to open the django built-in administration application that accept your superuser regstered in above step. Be sure path to administration screen has been changed from default value "admin" to "manahger" for security reason. And note that you can use `gunicorn --bind:0.0.0.0:8000 pbl.wsgi` instead of "manage.py" as similar to the production environment.

### Setup data for your test drive.
To prepare minimam data, follow below steps in the administration app.
 1. Add your several media files (should be a jpg or mp4) using "Media" menu.
 1. Create your own logic using "Logic" menu. be sure "default_logic" might be in the param field.
 1. Prep your logic using "Prep selected logics" menu in the Logic screen. This operation assigns relavant media files to the logic.
 1. Launch the application with "http://localhost:8000" and try to start your experiment using the logic you created.

## Install to the production environment.
 [Microsoft Azure](https://azure.microsoft.com) is a server-side production environment. Please note that the system will be deployed automatically when code has been comitted to the repository as "main" branch. So be sure to commit the code carefully. Regarding deployment to Azure, please read separated document [PRODUCTION.md](PRODUCTION.md) for further details.

## TO-DO.
I will try to handle following issues if I have a time...
1. Developing a new logic that uses keywords which participant specified in main screen as a kind of topic-related information, and retrieves media files from the internet. I have a plan to use [MediaWiki](https://www.mediawiki.org/) REST API and other resources to get relavant "free" movie files automatically.
1. Controls the order of "Logic" names on the main screen to choose easier by participants.
1. Isolate "prep" async task from django main thread to supports more complecated and time-consuming algorithms in the logic module. Using [django-background-tasks](https://django-background-tasks.readthedocs.io/)  could be a solution. Custom startup script in production also needed. Then "prep" might be start automatically also.
1. Current design of Logic.media_list is NOT safety and scalable. Reconsider data relationship between Logic and Trial.
1. Adding feature to support text (words) as a new media data.
1. Adding more logger to trace internal process. Obviously logging is super important for reliable system.
1. There is no test code. Yes, you are right. I understand it's unbelievable in 2020. I have to write some tests to cover vital part of this system. also should concider to CI and CD if the system improved continually.
1. Adding some transition effects in playback screen. I had try to add fancy effects using CSS animation features, but it was a bit complecated work for me...
1. Should I improve the user interface using fancy UI framework like Bootstrap or Vue ? I think Plain HTML5 and CSS might be enough for me at this stage...
1. Adding favicon and cool logo if somebody donated to me.

### Tips for you as a python/django developer.
1. To writing a readble Python.code, using [flake8](https://pypi.org/project/flake8/), [isort](https://pypi.org/project/isort/), and [black](https://github.com/psf/black) would be great. Not only for the IDE integration but also as an independent tool like "isort .". See also [pep8](https://pep8.readthedocs.io/en/).
1. To check current version of installed modules, use ```pip list --outdated```.

## Feedback
Pull requests, feature ideas and bug reports are very welcome!

## References
Many thanks for all authors of following usefull contents.
 - [Django on Azure - beyond "hello world"](https://tonybaloney.github.io/posts/django-on-azure-beyond-hello-world.html)
 - [DjangoにPostgreSQLを適用する](https://qiita.com/shigechioyo/items/9b5a03ceead6e5ec87ec)
 