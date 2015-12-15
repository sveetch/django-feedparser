# -*- coding: utf-8 -*-
"""
Feed renderers
"""
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string

import feedparser
import requests

from .utils import safe_import_module

class FeedBasicRenderer(object):
    """
    Feed renderer fetch the given url and render it using a template
    
    Django cache is used to avoid fetching again the same feed url, but the 
    feed render (when the fetching has been done) itself is not cached.
    """
    cache_key = settings.FEED_CACHE_KEY
    feed_context_name = 'feed_content'
    _template = settings.FEED_RENDERER_DEFAULT_TEMPLATE
    _timeout = settings.FEED_TIMEOUT
    _bozo_accept = settings.FEED_BOZO_ACCEPT
    _safe = settings.FEED_SAFE_FETCHING
    
    def __init__(self, *args, **kwargs):
        self.safe = kwargs.get('safe', self._safe)
        self.timeout = kwargs.get('timeout', self._timeout)
        self.bozo_accept = kwargs.get('bozo_accept', self._bozo_accept)
        self.default_template = kwargs.get('default_template', self._template)
        
        self._feed = None
    
    def fetch(self, url):
        """
        Get the feed content using 'requests'
        """
        try:
            r = requests.get(url, timeout=self.timeout)
        except requests.exceptions.Timeout:
            if not self.safe:
                raise
            else:
                return None
        
        # Raise 404/500 error if any
        if r and not self.safe:
            r.raise_for_status()
        
        return r.text

    def parse(self, content):
        """
        Parse the fetched feed content
        
        Feedparser returned dict contain a 'bozo' key which can be '1' if the feed 
        is malformed.
        
        Return None if the feed is malformed and 'bozo_accept' 
        is 'False', else return the feed content dict.
        
        If the feed is malformed but 'bozo_accept' is 'True', the feed content dict will 
        contain the parsing error exception informations in 'bozo_exception'.
        """
        if content is None:
            return None
        
        feed = feedparser.parse(content)
        
        # When feed is malformed
        if feed['bozo']:
            # keep track of the parsing error exception but as string 
            # infos, not an exception object
            exception_content = {
                "exception": str(type(feed['bozo_exception'])),
                "content": str(feed['bozo_exception'].getException()),
                "line": feed['bozo_exception'].getLineNumber(),
                "message": feed['bozo_exception'].getMessage(),
            }
            # Overwrite the bozo content from feedparser
            feed['bozo_exception'] = exception_content
            # bozo feeds are not accepted
            if not self.bozo_accept:
                feed = None

        return feed
    
    def get(self, url, expiration):
        """
        Fetch the feed if no cache exist or if cache is stale
        """
        # Hash url to have a shorter key and add it expiration time to avoid clash for 
        # other url usage with different expiration
        cache_key = self.cache_key.format(**{
            'id': hashlib.md5(url).hexdigest(),
            'expire': str(expiration)
        })
        
        # Get feed from cache if any
        feed = cache.get(cache_key)
        # Else fetch it
        if feed is None:
            #print "No feed cache, have to fetch it"
            feed = self.fetch(url)
            cache.set(cache_key, feed, expiration)
            
        return self.parse(feed)
    
    def format_feed_content(self, feed):
        """
        Formatter to post-process parsed feed
        
        This default method don't do anything but returning the parsed 
        feed. Custom renderer can implement its own formatter if needed.
        """
        return feed
    
    def get_context(self, url, expiration):
        """
        Build template context with formatted feed content
        """
        self._feed = self.get(url, expiration)
        
        return {
            self.feed_context_name: self.format_feed_content(self._feed),
        }
    
    def render(self, url, template=None, expiration=0):
        """
        Render feed template
        """
        template = template or self.default_template
        
        return render_to_string(template, self.get_context(url, expiration))


class FeedJsonRenderer(FeedBasicRenderer):
    """
    Basic renderer for JSON content
    
    Obviously don't use feedparser to parse it, instead just use ``json.loads(...)``
    to load the JSON string as Python object
    """
    def parse(self, content):
        """
        Just return fetched content, JSON dont need to be parsed here
        """
        if content is None:
            return None
        
        return json.loads(content)
