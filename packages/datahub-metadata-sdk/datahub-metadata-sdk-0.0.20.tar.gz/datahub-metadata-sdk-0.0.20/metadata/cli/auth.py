# -*- coding: utf-8 -*-

import logging
import os
from configparser import ConfigParser

from metadata.ensure import ensure_true
from metadata.context import MetadataContext
from metadata.exception import MetadataContextError, MetadataException
from metadata.utils.time import get_current_datetime
from metadata.utils.storage import TiefblueStorageClient

logger = logging.getLogger(__name__)
conf_path = os.path.expanduser('~%s/.metadata.ini' % os.getenv('SUDO_USER', ''))
default_section_name = 'default'


def load_config():
    config = ConfigParser()
    if os.path.exists(conf_path):
        logger.debug('%s found, parse before continue', conf_path)
        try:
            config.read(conf_path)
        except Exception as e:
            logger.warn('read config from %s error, remove before continue, %s', conf_path, e)
            os.remove(conf_path)

    if not config.has_section(default_section_name):
        config.add_section(default_section_name)
    return config

def save_config(config):
    with open(conf_path, 'w') as configfile:
        config.write(configfile)

def set_user_context(name, endpoint, token, project, user_email, *, bohrium_user, bohrium_password, bohrium_url, tiefblue_url):
    config = load_config()

    context_section_name = 'context.%s' % name
    if not config.has_section(context_section_name):
        config.add_section(context_section_name)

    config.set(context_section_name, 'endpoint', endpoint)
    config.set(context_section_name, 'token', token)
    config.set(context_section_name, 'project', project)
    config.set(context_section_name, 'user', user_email)
    config.set(context_section_name, 'bohrium_user', bohrium_user)
    config.set(context_section_name, 'bohrium_password', bohrium_password)
    config.set(context_section_name, 'bohrium_url', bohrium_url)
    config.set(context_section_name, 'tiefblue_url', tiefblue_url)
    config.set(context_section_name, 'added_time', str(get_current_datetime()))

    config.set(default_section_name, 'current_context', name)
    save_config(config)

def remove_user_context_conf(name):
    config = load_config()

    context_section_name = 'context.%s' % name
    if config.has_section(context_section_name):
        config.remove_section(context_section_name)

    if config.get(default_section_name, 'current_context') == name:
        config.remove_option(default_section_name, 'current_context')
    save_config(config)

def switch_user_context_conf(name):
    config = load_config()

    context_section_name = 'context.%s' % name
    if not config.has_section(context_section_name):
        raise MetadataContextError('context %s not found' % name)

    config.set(default_section_name, 'current_context', name)
    save_config(config)

def get_current_context_conf():
    if not os.path.exists(conf_path):
        return
    config = load_config()
    name = config.get(default_section_name, 'current_context')
    if name:
        context_section_name = 'context.%s' % name
        return dict(config.items(context_section_name))

def get_context_from_conf(conf):
    conf = dict(conf) if isinstance(conf, list) else conf
    endpoint = conf.get('endpoint')
    token = conf.get('token')
    project = conf.get('project')
    bohrium_user = conf.get('bohrium_user')
    bohrium_password = conf.get('bohrium_password')
    bohrium_url = conf.get('bohrium_url')
    tiefblue_url = conf.get('tiefblue_url')
    if not endpoint or not token:
        return
    storage_client = TiefblueStorageClient(bohrium_user, bohrium_password,
        bohrium_endpoint=bohrium_url,
        tiefblue_endpoint=tiefblue_url)
    return MetadataContext(endpoint, token, project=project, storage_client=storage_client)

def purge_user_context():
    if os.path.exists(conf_path):
        os.remove(conf_path)