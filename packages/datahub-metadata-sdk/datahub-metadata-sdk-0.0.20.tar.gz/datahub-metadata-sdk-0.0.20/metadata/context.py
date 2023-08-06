# -*- coding: utf-8 -*-

import os
import copy
import logging
import contextlib
from functools import partial, wraps, cached_property
import urllib3
import threading
from typing import Mapping, Any, Optional
from urllib.parse import urljoin
from http.client import HTTPConnection
from urllib3.exceptions import InsecureRequestWarning

import backoff
import requests
from requests.exceptions import ConnectionError
from datahub.emitter.rest_emitter import DatahubRestEmitter                                                                                                                                                                            

from metadata.exception import MetadataContextError
from metadata.consts import ENV_TYPE
from metadata.utils.url import build_url
from metadata.utils.storage import StorageClient
from metadata.ensure import (
    ensure_endpoint_format, ensure_token_format, 
    ensure_project_format, ensure_env_enum,
    )

local = threading.local()
logger = logging.getLogger(__name__)
urllib3.disable_warnings(category=InsecureRequestWarning)

__all__ = ['MetadataContext', 'get_current_context']


class MetadataContext(object):

    def __init__(self, endpoint: Optional[str]=None, token: Optional[str]=None, *,
            project: str='default',
            env=ENV_TYPE.CORP,
            options: Optional[Mapping[str, Any]]=None,
            storage_client: Optional[StorageClient]=None):

        endpoint = endpoint or os.getenv('DATAHUB_GMS_URL')
        token = token or os.getenv('DATAHUB_GMS_TOKEN')

        endpoint = ensure_endpoint_format(endpoint)
        token = ensure_token_format(token)
        ensure_project_format(project)
        ensure_env_enum(env)
        self.endpoint = build_url(endpoint, '')
        self.token = token
        if not self.token:
            raise MetadataContextError('token required')
        self.project = project
        self.env = env

        self.http_session = requests.session()
        self.emitter = DatahubRestEmitter(gms_server=build_url(endpoint, ''), token=token,  extra_headers={})    
        self.emitter.test_connection()

        self.started = False
        self.debug = False
        self.options = self._load_options(**(options or {}))

        self.storage_client = storage_client

    @staticmethod
    def _load_options(**kwargs):
        options = {
            'defaults.metadata.context.debug_requests_response': False,
            'defaults.metadata.context.request_timeout': (10, 60),
            'defaults.metadata.context.debug_context_state': False,
            'defaults.metadata.client.sync_wait': True,
            'defaults.metadata.client.sync_wait_timeout': 30,
            'defaults.metadata.client.sync_wait_interval': 1,
            'defaults.metadata.context.backoff_when_get_502': True,
            'defaults.metadata.context.backoff_max_seconds': 30,
            'defaults.metadata.context.backoff_when_connection_error': False,
            'defaults.metadata.context.backoff_connection_error_max_seconds': 30,
        }
        for k in list(options.keys()):
            env = k.upper().replace('.', '_')
            if os.getenv(env) is not None:
                options[k] = eval(os.getenv(env))
        options.update(kwargs)
        return options

    def __enter__(self):
        if self.started:
            raise MetadataContextError('%s already started' % self)
        global local
        contexts = getattr(local, 'contexts', [])
        contexts.append(self)
        setattr(local, 'contexts', contexts)
        if self.options.get('defaults.metadata.context.debug_context_state', None):
            print('%s) context %s __enter__' % (threading.get_ident(), self))
        self.started = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if not self.started:
            raise MetadataContextError('%s not start' % self)
        global local
        contexts = getattr(local, 'contexts', [])
        if contexts:
            popped = contexts.pop()
            if popped != self:
                raise MetadataContextError('popped context order does not match what added')
            if self.options.get('defaults.metadata.context.debug_context_state', None):
                print('%s) context %s __exit__' % (threading.get_ident(), self))
        else:
            raise MetadataContextError('popped context order does not match what added, contexts is empty')
        self.started = False
        setattr(local, 'contexts', contexts)

    def stop(self):
        return self.__exit__(None, None, None)

    def start(self):
        return self.__enter__()

    def __str__(self):
        return "<{self.__class__.__name__}(endpoint={self.endpoint})>".format(self=self)

    def request(self, method, url, stream=False, **kwargs):
        func = self._request
        if method.lower() == 'get':
            if self.options.get('defaults.metadata.context.backoff_when_connection_error'):
                max_time = self.options.get('defaults.metadata.context.backoff_connection_error_max_seconds', 30)
                func = backoff.on_exception(backoff.expo,
                                            requests.ConnectionError,
                                            max_time=max_time,
                                            logger=logger,
                                            )(func)
            if self.options.get('defaults.metadata.context.backoff_when_get_502'):
                max_time = self.options.get('defaults.metadata.context.backoff_max_seconds', 30)
                func = backoff.on_predicate(backoff.expo,
                                            lambda r: r.status_code == 502,
                                            max_time=max_time,
                                            logger=logger,
                                            )(func)

        return func(method, url, stream=stream, **kwargs)

    def _request(self, method, url, stream=False, **kwargs):
        url = urljoin(str(self.endpoint), str(url))
        kwargs['verify'] = False
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.options.get('defaults.metadata.context.request_timeout', (3, 10))
        headers = copy.deepcopy(self.http_session.headers)
        if stream:
            headers['Content-Type'] = 'text/plain;charset=UTF-8'
        else:
            headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {self.token}'
        headers.update(kwargs.pop('headers', {}))
        response = self.http_session.request(method, url, headers=headers, stream=stream, **kwargs)
        if kwargs.pop('raise_for_status', True):
            response.raise_for_status()

        if self.options.get('defaults.metadata.context.debug_requests_response'):
            from pprint import pprint
            pprint(response.text if not stream else response)
        return response

    def debug_requests_on(self):
        self.debug = True
        HTTPConnection.debuglevel = 1
        root_logger = logging.getLogger('metadata')
        root_logger.setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        self.options['defaults.metadata.context.debug_requests_response'] = True

    def debug_requests_off(self):
        self.debug = False
        HTTPConnection.debuglevel = 0
        root_logger = logging.getLogger('metadata')
        root_logger.setLevel(logging.WARNING)
        root_logger.handlers = []
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = False
        self.options['defaults.metadata.context.debug_requests_response'] = False

    @contextlib.contextmanager
    def debug_requests(self):
        self.debug_requests_on()
        yield
        self.debug_requests_off()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    @property
    def user_name(self):
        return self.user_email.split('@')[0]

    @property
    def user_email(self):
        return self.user['username']

    @cached_property
    def user(self):
        return self.client._get_current_user()
        
    @cached_property
    def client(self):
        from metadata.client.client import Client
        return Client(self)


def get_current_context() -> MetadataContext:
    global local
    contexts = getattr(local, 'contexts', [])
    if not contexts:
        try:
            from metadata.cli.auth import get_context_from_conf, get_current_context_conf
            conf = get_current_context_conf()
            if not conf:
                return
            context = get_context_from_conf(conf)
            if context:
                contexts = [context]
                setattr(local, 'contexts', contexts)
        except Exception as e:
            raise
            logger.warn('found invalid context, take `metadata login` to refresh context, %s', e)
    return contexts[-1] if contexts else None