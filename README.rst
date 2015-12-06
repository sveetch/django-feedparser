.. _Django: https://www.djangoproject.com/
.. _feedparser: https://github.com/kurtmckee/feedparser
.. _requests: http://docs.python-requests.org/

=================
django-feedparser
=================

A `Django`_ app using `feedparser`_ to fetch and parse a feed to render it from a template. 

It is not a Feed agregator since it manage feeds one by one.

* `requests`_ is used to fetch feeds;
* `feedparser` is used to parse feeds;
* Django cache is used to avoid fetching again the feed each time;
* Basic feed renderer just parse the feed without modifying anything but you can extend it to implement your post-process formatting;
* Once the feed has been fetched, it can be displayed through a template. Default template is really basic and you should eventually override it or create another one to fit to your feed structure/format;

Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/django-feedparser>`_;
* Clone it on his `repository <https://github.com/emencia/django-feedparser>`_;

Requires
********

* `Django`_ >= 1.4;
* `requests`_ >= 2.7.0',
* `feedparser`_ >= 5.1.3',

Install
*******

First install the package: ::

    pip install django-feedparser

Add it to your installed Django apps in settings: ::

    INSTALLED_APPS = (
        ...
        'django_feedparser',
        ...
    )

Then import its settings: ::

    from django_feedparser import *

And finally see about `Available settings`_ your can override.

Usage
*****

Views
-----

There is a mixin ``django_feedparser.views.FeedFetchMixin`` you can inherit from your views to exploit a feed.

And there is a basic view ``django_feedparser.views.FeedView`` that inherits from mixin ``FeedFetchMixin`` to demonstrate its usage. However the basic view is usable as it if it meets your needing, if so you just have to use it directly in your urls like ``django.views.generic.base.TemplateView``: ::
    
    from django.conf.urls import *

    from .views import FeedView

    urlpatterns = patterns('',
        ...
        url(r'^myfeed/$', FeedView.as_view(feed_url="http://localhost/myfeed.xml"), name="myfeed"),
        ...
    )

.. NOTE::
   Although the app contains an 'urls.py', it's mainly intended for debugging purpose, you should not mount it in your project urls.

Template tags
-------------

More common way is to use the template tag to include rendered feed in your templates.

Basic sample: ::

    {% load feedparser_tags %}
    {% feedparser_render 'http://localhost/sample.xml' %}

Or with all accepted arguments: ::

    {% feedparser_render 'http://localhost/sample.xml' renderer='CustomRenderer' template='foo/custom.html' expiration=3600 %}


Available settings
******************

FEED_RENDERER_DEFAULT_TEMPLATE
    Path to the default renderer template.
    
    **Default value**: ``'django_feedparser/basic_feed_renderer.html'``

FEED_CACHE_KEY
    Feed cache key template string.
    
    **Default value**: ``'feedparser_feed_{id}_{expire}'``

FEED_TIMEOUT
    Timeout until feed response, in seconds.
    
    **Default value**: ``5``

FEED_BOZO_ACCEPT
    Wether we accept (``True``) badly formatted xml feed or not (``False``).
    
    **Default value**: ``True``

FEED_SAFE_FETCHING
    Wether bad http status or request error will throw an exception (``False``) or not (``True``).
    
    **Default value**: ``True``

FEED_RENDER_ENGINES
    A Python dictionnary for available renderer engines, where the key is the shortcut 
    engine name and the value is a valid Python path to the renderer class.
    
    **Default value**: ::
    
        {
            'basic': 'django_feedparser.renderer.FeedBasicRenderer',
        }
