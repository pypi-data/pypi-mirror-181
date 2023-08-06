# -*- coding: utf-8 -*-

import os
import logging

from metadata.utils.format import format_table
from metadata.cli.auth import (
    load_config, switch_user_context_conf, remove_user_context_conf,
    get_current_context_conf, purge_user_context,
)

logger = logging.getLogger(__name__)
default_section_name = 'default'


def do_context(args):
    if args.list:
        config = load_config()
        properties = []
        if not config.has_section(default_section_name):
            return
        if not config.has_option(default_section_name, 'current_context'):
            return
        current_context_name = config.get(default_section_name, 'current_context')
        for section_name in config.sections():
            if section_name.startswith('context.'):
                name = section_name[len('context.'):]
                conf = dict(config.items(section_name))
                properties.append((
                    'On' if current_context_name == name else '',
                    name, conf.get('endpoint'), conf.get('user'), conf.get('project'), conf.get('bohrium_user')))
        print(format_table(['Active', 'Name', 'Endpoint', 'User', 'Project', 'Bohrium User'], properties))
        return
    elif args.switch:
        switch_user_context_conf(args.switch)
    elif args.remove:
        remove_user_context_conf(args.remove)
    elif args.clear:
        purge_user_context()
    else:
        conf = get_current_context_conf()
        if not conf:
            return
        endpoint = conf.get('endpoint')
        user_email = conf.get('user')
        print(f'Endpoint: {endpoint}')
        print(f'Username: {user_email}')