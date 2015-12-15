# -*- coding: utf-8 -*-
"""
Snippet template tags
"""
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

from django_feedparser.utils import FeedparserError, get_feed_renderer

register = template.Library()

@register.simple_tag
def feedparser_render(url, *args, **kwargs):
    """
    Render a feed and return its builded html
    
    Usage: ::
    
        {% feedparser_render 'http://localhost/sample.xml' %}
    
    Or with all accepted arguments: ::
    
        {% feedparser_render 'http://localhost/sample.xml' renderer='CustomRenderer' template='foo/custom.html' expiration=3600 %}
    """
    renderer_name = kwargs.get('renderer', settings.FEED_DEFAULT_RENDERER_ENGINE)
    renderer_template = kwargs.get('template', None)
    expiration = kwargs.get('expiration', 0)
    
    renderer = get_feed_renderer(settings.FEED_RENDER_ENGINES, renderer_name)
    return renderer().render(url, template=renderer_template, expiration=expiration)
