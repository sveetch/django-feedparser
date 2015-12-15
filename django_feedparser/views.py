# -*- coding: utf-8 -*-
"""
App views
"""
#from django.db import models
from django.conf import settings
from django.views import generic

from .utils import FeedparserError, get_feed_renderer

class FeedFetchMixin(object):
    """
    Mixin to contain all feed fetching stuff
    """
    feed_renderer_name = settings.FEED_DEFAULT_RENDERER_ENGINE
    feed_url = None
    feed_template = None
    feed_cache_expiration = 0
    
    def get_feed_url(self):
        if getattr(self, 'feed_url', None) is None:
            raise FeedparserError("'{}' must define 'feed_url'".format(self.__class__.__name__))
        return self.feed_url
    
    def get_feed_renderer(self):
        renderer = get_feed_renderer(settings.FEED_RENDER_ENGINES, self.feed_renderer_name)
        
        return renderer
    
    def render_feed(self, renderer, url):
        return renderer().render(url, template=self.feed_template, expiration=self.feed_cache_expiration)


class FeedView(FeedFetchMixin, generic.TemplateView):
    """
    View test for feedparser usage
    """
    template_name = "django_feedparser/view.html"
    
    def get_context_data(self, **kwargs):
        context = super(FeedView, self).get_context_data(**kwargs)
        
        feed_url = self.get_feed_url()
        feed_renderer = self.get_feed_renderer()
        
        context['feed_url'] = feed_url
        context['feed_rendered'] = self.render_feed(feed_renderer, feed_url)
        
        return context
