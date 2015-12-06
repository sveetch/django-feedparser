# -*- coding: utf-8 -*-
"""
Default app settings
"""
# Path to the default renderer template
FEED_RENDERER_DEFAULT_TEMPLATE = "django_feedparser/basic_feed_renderer.html"

# Feed cache key template string
FEED_CACHE_KEY = 'feedparser_feed_{id}_{expire}'

# Timeout until feed response
FEED_TIMEOUT = 5

# Wether we accept (True) badly formatted xml feed or not (False)
FEED_BOZO_ACCEPT = True

# Wether bad http status or request error will throw an exception (False) or not (True)
FEED_SAFE_FETCHING = True

# Available renderer engines
FEED_RENDER_ENGINES = {
    'basic': 'django_feedparser.renderer.FeedBasicRenderer',
}