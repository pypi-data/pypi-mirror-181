

import urllib
import pickle

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache.backends.base import BaseCache
from django.core.cache import caches
from django.conf import settings

from orpc_client import OrpcConnectionPool


def get_first_zencache_namespace():
    for name, info in settings.CACHES.items():
        klass = info.get("class")
        if klass == "django_zencache.DjangoZenCache":
            return name
    return "default"


def get_connection(namespace=None):
    namespace = namespace or get_first_zencache_namespace()
    cache = caches[namespace]
    cache_pool = cache.cache_pool
    session = cache_pool.get_session()
    service = session.zencache
    return service


class DjangoZenCache(BaseCache):
    def __init__(self, location, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hostinfo = urllib.parse.urlparse("zc://{host}".format(host=location))
        self.host = hostinfo.hostname
        self.port = hostinfo.port
        if args:
            params = args[0]
            options = params.get("OPTIONS", {})
            self.default_timeout = params.get("TIMEOUT", None)
        else:
            options = {}
            self.default_timeout = None
        options = dict([[k.lower(), v] for k, v in options.items()])
        self.pool_size = options.get("pool_size", 10)
        self.username = options.get("username", None)
        self.password = options.get("password", None)
        self.auto_login = options.get("auto_login", self.username and self.password and True or False)
        self.auto_reconnect = options.get("auto_reconnect", True)
        self.buffer_size = options.get("buffer_size", None)
        self.rfile_buffer_size = options.get("rfile_buffer_size", None)
        self.wfile_buffer_size = options.get("wfile_buffer_size", None)
        self.password_hash_method = options.get("password_hash_method", None)
        self.cache_pool = OrpcConnectionPool(self.pool_size, kwargs={
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "login_event": "zencache.login",
            "auto_login": self.auto_login,
            "auto_reconnect": self.auto_reconnect,
            "buffer_size": self.buffer_size,
            "rfile_buffer_size": self.rfile_buffer_size,
            "wfile_buffer_size": self.wfile_buffer_size,
            "password_hash_method": self.password_hash_method,
        })
    
    @property
    def session(self):
        return self.cache_pool.get_session()

    def _encode(self, value):
        return pickle.dumps(value)
    
    def _decode(self, data):
        return pickle.loads(data)
    
    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout is DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        key = self.make_key(key, version=version)
        self.validate_key(key)
        value = self._encode(value)
        session = self.session
        session.zencache.set(key, value)
        if timeout:
            session.zencache.expire(key, timeout)
        return True

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        session = self.session
        result = session.zencache.get(key)
        if result is None:
            return default
        else:
            result = self._decode(result)
            return result

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout is DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        key = self.make_key(key, version=version)
        self.validate_key(key)
        value = self._encode(value)
        session = self.session
        session.zencache.set(key, value)
        if timeout:
            session.zencache.expire(key, timeout)

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout is DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        key = self.make_key(key, version=version)
        self.validate_key(key)
        if timeout:
            self.session.zencache.expire(key, timeout)
        return True

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        self.session.zencache.delete(key)
        return True

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return self.session.zencache.exists(key)

    def clear(self):
        return self.session.zencache.flushall()
