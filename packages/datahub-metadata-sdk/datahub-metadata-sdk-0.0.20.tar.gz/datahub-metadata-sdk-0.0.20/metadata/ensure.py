# -*- coding: utf-8 -*-

import jwt
import sys
import logging
import validators
from datetime import datetime
from tzlocal import get_localzone
from dateutil import parser

from metadata.exception import (
    MetadataValueError, MetadataContextError,
    MetadataAssertionError, MetadataTypeError,
)
from metadata.utils.time import timestamp_to_datetime, datetime_to_timestamp

logger = logging.getLogger(__name__)


def ensure_token_format(token):
    try:
        jwt.decode(token, verify=False, algorithms='HS256', options={"verify_signature": False})
    except:
        raise MetadataValueError('Token format error')
    return token

def ensure_endpoint_format(endpoint):
    if validators.url(endpoint, public=True) is not True:
        raise MetadataContextError('Invalid endpoint')
    return endpoint

def ensure_entity_urn_format(urn):
    return urn

def ensure_entity_name_format(name):
    return name

def ensure_env_format(env):
    return env

def ensure_project_format(project):
    return project

def ensure_uri_format(uri):
    return uri

def ensure_platform_format(platform):
    return platform

def ensure_env_enum(env):
    return env

def ensure_true(condition, message, exc_type=MetadataAssertionError, *args, **kwargs):
    raise_only = kwargs.pop('raise_only', True)
    if not condition:
        if not message:
            message = 'condition check failed'
        else:
            message = message.format(*args, **kwargs)
        logger.error(message)
        if raise_only:
            raise exc_type(message)
        else:
            sys.exit(1)


def ensure_type(obj, types, message=None, exc_type=MetadataTypeError, **kwargs):
    if not isinstance(obj, types):
        if not message:
            message = 'required type(%s) but (%s:%s) found' % (types, obj, type(obj))
        else:
            message = message.format(**kwargs)
        logger.error(message)
        raise exc_type(message)

def ensure_timestamp(obj, precision='ms', _round=True):
    if isinstance(obj, datetime):
        return datetime_to_timestamp(obj, precision, _round)
    if isinstance(obj, str):
        obj = parser.parse(obj)
        return datetime_to_timestamp(obj, precision, _round)
    dt = timestamp_to_datetime(obj)
    return datetime_to_timestamp(dt, precision, _round)

def ensure_datetime(obj, precision='us'):
    if isinstance(obj, datetime):
        return obj
    if isinstance(obj, str):
        t = parser.parse(obj)
        return t.astimezone(get_localzone())
    obj = ensure_timestamp(obj, precision=precision)
    return timestamp_to_datetime(obj)

def ensure_id(obj):
    if obj == 'unknown':
        raise ValueError('id must set')

def ensure_flow_urn(obj):
    if obj == 'unknown':
        raise ValueError('flow_urn must set')
