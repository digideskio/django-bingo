django-bingo
------------

django-bingo is a bingo app to play bingo games like "bullshit bingo" while listening together to some radio show and marking the words, which were mentioned.

Dependencies
------------

Python packages:

* django 1.8
* django-jquery 1.9.1
* django-colorful 0.1.3
* pytz 2013b
* pillow 2.1.0

For SSE:

* sse 1.2
* redis 2.10.3
* flask 0.10.1
* gevent 1.0.2

Other: a ttf-file as font for the image-export.

Installing
----------

Create a django project. Then add the following options to your settings.py

* append to ```INSTALLED_APPS``` (make sure ``bingo`` is included first)
    * 'bingo'
    * 'jquery'
    * 'colorful'
    * 'registration'
* ```FONT_PATH``` = '/path/to/font.ttf'

Include the bingo-app in your project urls.py, like this:
```url(r'^', include('bingo.urls'))```
Include the ```registration``` app like this:
```url(r'^accounts/', include('registration.backends.simple.urls'))```

Registration is only tested with the ```simple``` backend.
You can use other ```django-registration``` backends, but you will need to add additional templates and views.

You can use the Sites framework to add several different Bingo sites.
Different Sites have different sets of Words, and they will generate a different set of Games, so the Bingos are independend from each other.

Upgrading
---------

For upgrading from an older version you may need to use ```manage.py migrate```, if the database scheme was changed.

When upgrading from versions prior to 1.4, upgrade first using ``south`` and ```django 1.6```. Then upgrade to the current version using the django migrations.

Settings
--------

#### required settings

* ```TEMPLATE_CONTEXT_PROCESSORS```: add the [default context_processors](https://docs.djangoproject.com/en/1.5/ref/settings/#template-context-processors),  and then the django-bingo context_processor ```bingo.context_processors.bingo```.
* ```FONT_PATH``` the ttf font used to generate images.
* at least one of
    * ```GAME_HARD_TIMEOUT``` time after which a game is stopped
    * ```GAME_SOFT_TIMEOUT``` time after which a game without any activity is stopped

#### optional settings

see CONFIGURATION.md

Customizing
-----------

Many minor changes can be done with project templates:

* install [django-apptemplates](https://pypi.python.org/pypi/django-apptemplates/) and add it to the ```TEMPLATE_LOADER``` setting.
* add an own templates directory to ```TEMPLATE_DIRS```.
* create custom templates, which inherit from the app templates.

example for "mytemplates/bingo/main.html":

    {% extends "bingo:bingo/base.html %}
    {% block extra_content_top %}Welcome to my bingo game!{% endblock %}
