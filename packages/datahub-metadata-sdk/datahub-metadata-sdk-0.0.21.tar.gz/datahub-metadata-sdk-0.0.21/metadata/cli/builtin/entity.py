# -*- coding: utf-8 -*-

import json
import logging
import dataclasses
from abc import ABCMeta, abstractmethod
from argparse import Namespace
from typing import Mapping, Any

from metadata.ensure import ensure_true
from metadata.utils.edit import system_edit
from metadata.utils.format import yaml2json, dict2yaml, dict2json
from metadata.exception import MetadataError
from metadata.client.client import Client
from metadata.context import MetadataContext

logger = logging.getLogger(__name__)


class IEntity(object, metaclass=ABCMeta):

    name = NotImplemented
    scope = 'project'
    candidate_names = NotImplemented
    container_type = NotImplemented

    @classmethod
    @abstractmethod
    def get_one_func(cls, client: Client):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_multi_func(cls, client: Client):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete_one_func(cls, client: Client):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create_one(cls, client: Client, dt: Mapping[str, Any]):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update_one(cls, client: Client, dt: Mapping[str, Any]):
        raise NotImplementedError

    @classmethod
    def parse_kwargs(cls, args: Namespace):
        tags = getattr(args, 'tags') or ''
        tags = tags.split(',') if tags else None
        kwargs = {
            'start': args.start,
            'count': min(args.limit, 200),
            'tags': tags,
        }
        return kwargs

    @classmethod
    def do_get(cls, context: MetadataContext, args: Namespace, urn: str=None):
        client = context.client
        if urn:
            return cls.get_one_func(client)(urn)

        kwargs = cls.parse_kwargs(args)

        if args.output:
            return cls.get_multi_func(client)(**kwargs)

        if args.fields:
            keys = args.fields.split(',')
        else:
            keys = list(cls.get_property_keys())

        properties = []
        for tb in cls.get_multi_func(client)(**kwargs):
            item = [getattr(tb, key) for key in keys]
            properties.append(item)
        return keys, properties

    @classmethod
    def do_delete(cls, context: MetadataContext, args: Namespace, urn: str):
        client = context.client
        if cls.container_type == 'container':
            cls.delete_one_func(client)(urn, soft=not args.hard, cascade=args.cascade)
        else:
            cls.delete_one_func(client)(urn, soft=not args.hard)
        logger.info('delete entity %s/%s successfully' % (cls.name, urn))

    @classmethod
    def get_property_keys(cls):
        return ['urn', 'display_name', 'entity_type']

    @classmethod
    def do_create(cls, context: MetadataContext, args: Namespace, dt: Mapping[str, Any]):
        client = context.client
        urn = cls.create_one(client, dt)
        logger.info('create resource %s/%s successfully' % (cls.name, urn))

    @classmethod
    def do_update(cls, context: MetadataContext, args: Namespace, urn: str, dt: Mapping[str, Any]):
        ensure_true(urn or dt.get('urn'), 'Update urn required')
        client = context.client
        dt.pop('entity_type', None)
        dt['urn'] = urn or dt.get('urn')
        urn = cls.update_one(client, dt)
        logger.info('create resource %s/%s successfully' % (cls.name, urn))

    @classmethod
    def do_edit(cls, context: MetadataContext, args: Namespace, urn: str):
        client = context.client
        res = cls.get_one_func(client)(urn)
        if not res:
            logger.error(f'entity with urn={urn} not found')
            return
        try:
            if args.output == 'yaml':
                dt = json.loads(yaml2json(system_edit(dict2yaml(dataclasses.asdict(res)))))
            else:
                dt = json.loads(system_edit(dict2json(dataclasses.asdict(res))))
        except MetadataError:
            logger.info('update canceled successfully')
            return
        dt.pop('entity_type', None)
        urn = cls.update_one(client, dt)
        logger.info('update resource %s/%s successfully' % (cls.name, urn))