# -*- coding: utf-8 -*-
"""
App URLs for development purpose
"""
from django.conf.urls import *

from .views import FeedView

urlpatterns = patterns('',
    url(r'^$', FeedView.as_view(feed_url = "http://192.168.0.103/feedtests/feed_title.xml"), name="index"),
    url(r'^ill/$', FeedView.as_view(feed_url = "http://192.168.0.103/feedtests/aaa_illformed.xml"), name="feed-ill"),
    url(r'^well/$', FeedView.as_view(feed_url = "http://192.168.0.103/feedtests/feed_title.xml"), name="feed-well"),
    url(r'^no_given_url/$', FeedView.as_view(feed_url=None), name="feed-nogivenurl"),
    url(r'^404/$', FeedView.as_view(feed_url = "http://192.168.0.103/feedtests/404.xml"), name="feed-404"),
    url(r'^404/raise/$', FeedView.as_view(feed_url = "http://192.168.0.103/feedtests/404.xml"), name="feed-404-raise"),
    url(r'^bad_renderer_path/$', FeedView.as_view(feed_url="http://192.168.0.103/feedtests/feed_title.xml", feed_renderer_name="wrong-path"), name="feed-bad_renderer_path"),
    url(r'^bad_renderer_name/$', FeedView.as_view(feed_url="http://192.168.0.103/feedtests/feed_title.xml", feed_renderer_name="wrong-name"), name="feed-bad_renderer_name"),
)
