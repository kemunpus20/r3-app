# Note

## To-do and ideas list
I will try to handle following issues if I have a time...
1. Isolate "Prep" task from Django main thread to supports more complecated and time-consuming algorithms in the logic module. Using [django-background-tasks](https://django-background-tasks.readthedocs.io/) could be a solution. may be a custom startup script for production environment also needed, and then "Prep" might be start automatically.
1. Obviously current design of Logic.media_list is neither safety nor scalable. So to reconsider data relationship between Logic and Trial once again.
1. To add more logger for trouble shooting in production environment.
1. To add more comments based on the Python docstrings style.
1. There is no test code. Yes, I understand, it's unbelievable in 2020. I have to write some tests to cover vital part of this system. And someday to concider to CI and CD if the system improved continually.
1. To add transition effects in playback screen. I had try to add fancy effects using CSS animation features, but it was a bit complecated work for me...
1. Should I improve the user interface using fancy UI framework like Bootstrap or Vue ? I think Plain HTML5 and CSS might be enough for me at this stage...
1. Adding favicon and cool logo if somebody donated to me.
1. To improve system overall performance, concider to use the smart cache mechanism in both Django and Azure.
1. Using Azure Private VNET would be better for security.

## Tips for Python / Django
1. To writing reliable Python code, [flake8](https://pypi.org/project/flake8/), [isort](https://pypi.org/project/isort/), and [black](https://github.com/psf/black) would be great tool. Not only for the IDE integration but also as an independent tool. See also [pep8](https://pep8.readthedocs.io/).
1. To checking current version of installed python modules, use ```pip list --outdated```.
1. To confirm Django application settings, `manage.py check --deploy` will provides some security related information. In addition, I had enabled all HSTS settings in settings.py, but did not work correctly. I suppose some of redirect-related configuration might be also necessaly. I think that my azure production enviroment is almost secure even if HSTS is disabled, so I have skipped this issue.
