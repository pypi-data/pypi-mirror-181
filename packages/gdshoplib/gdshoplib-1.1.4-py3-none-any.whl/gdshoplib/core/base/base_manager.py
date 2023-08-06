import functools
import logging

import requests as r

from gdshoplib.core.cache import BaseCache

logger = logging.getLogger(__name__)


class BaseManager:
    DESCRIPTION_TEMPLATE = "basic.txt"
    KEY = None

    def __init__(self) -> None:
        self.settings = self.SETTINGS()
        if self.settings.CACHE:
            self.CACHE = BaseCache.get_class(self.settings.CACHE_CLASS)(
                dsn=self.settings.CACHE_DSN, cache_period=self.settings.CACHE_PERIOD
            )

    def get_cache_key(self, path, **kwargs):
        return f"{path}"

    def check_cacheble(self, *args, **kwargs):
        return kwargs.get("method").upper() == "GET"

    def auth(self):
        raise NotImplementedError

    def cache_response(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if self.settings.CACHE and self.check_cacheble(*args, **kwargs):
                cache_key = self.get_cache_key(*args, **kwargs)
                cached = self.CACHE.get(cache_key)

                if cached:
                    return cached
                response = func(self, *args, **kwargs)
                if response.ok:
                    self.CACHE[cache_key] = response

                return self.CACHE[cache_key]
            return func(self, *args, **kwargs)

        return wrap

    @cache_response
    def make_request(self, path, *, method, params=None):
        _path = f"{self.BASE_URL}{path}"
        _params = (
            dict(params=params) or {}
            if method.upper() == "GET"
            else dict(json=params) or {}
        )

        _r = r.request(
            method,
            _path,
            headers=self.get_headers(),
            **_params,
        )
        if not _r.ok:
            logger.warning(_r.json())
            assert (
                False
            ), f"Запрос {method.upper()} {_path} прошел с ошибкой {_r.status_code}/n"

        return _r.json()

    def pagination(self, url, *, params=None, **kwargs):
        _params = params or {}
        response = None
        while True:
            response = self.make_request(url, params=_params, **kwargs)
            next_cursor = self.pagination_next(response)

            if next_cursor is None or next_cursor is False:
                return response
            else:
                return self.pagination(
                    url, params={**_params, **dict(start_cursor=next_cursor)}, **kwargs
                )

    def pagination_next(self, response):
        """Выдаем данные для следующего"""
        if not response:
            return None

        if not response.get("has_more"):
            return False

        return response["next_cursor"]
