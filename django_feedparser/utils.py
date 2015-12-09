# -*- coding: utf-8 -*-
import warnings

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from django.core.exceptions import ImproperlyConfigured

class FeedparserError(ImproperlyConfigured):
    pass

def safe_import_module(path, default=None):
    """
    Try to import the specified module from the given Python path
    
    @path is a string containing a Python path to the wanted module, @default is 
    an object to return if import fails, it can be None, a callable or whatever you need.
    
    Return a object or None
    """
    if path is None:
        return default
    
    dot = path.rindex('.')
    module_name = path[:dot]
    class_name = path[dot + 1:]
    try:
        _class = getattr(import_module(module_name), class_name)
        return _class
    except (ImportError, AttributeError) as e:
        raise FeedparserError("{}: {}".format(e.__class__.__name__, e.message))
    
    return default

def get_feed_renderer(engines, name):
    """
    From engine name, load the engine path and return the renderer class
    
    Raise 'FeedparserError' if any loading error
    """
    if name not in engines:
        raise FeedparserError("Given feed name '{}' does not exists in 'settings.FEED_RENDER_ENGINES'".format(name))
    
    renderer = safe_import_module(engines[name])
    
    return renderer
