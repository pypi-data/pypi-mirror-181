# -*- coding: utf-8 -*-

import os
from os.path import exists
from argparse import Namespace
from typing import Mapping, Any
from jsonpath_ng import parse

from metadata.utils.format import gen_tree_files, dict2json, dict2yaml, sizeof_fmt, format_table
from metadata.context import MetadataContext
from metadata.entity.model import Model
from metadata.cli.builtin.entity import IEntity
from metadata.client.client import Client


class IModel(IEntity):

    name = 'model'
    candidate_names = ['md']
    container_type = 'element'

    @classmethod
    def get_property_keys(cls):
        return super().get_property_keys() + ['uri']

    @classmethod
    def get_one_func(cls, client: Client):
        return client.get_model

    @classmethod
    def get_multi_func(cls, client: Client):
        def wraps(*args, **kwargs):
            return [client.get_model(urn) for urn in client.get_models_by_facts(*args, **kwargs)]
        return wraps

    @classmethod
    def delete_one_func(cls, client: Client):
        return client.delete_model

    @classmethod
    def create_one(cls, client: Client, dt: Mapping[str, Any]):
        dt.pop('entity_type', None)
        model = Model(**dt)
        return client.create_model(model)

    @classmethod
    def update_one(cls, client: Client, dt: Mapping[str, Any]):
        model = Model(**dt)
        return client.update_model(model)

    @classmethod
    def do_download(cls, context: MetadataContext, args: Namespace, urn: str):
        dest = args.dest
        if not exists(dest):
            os.makedirs(dest)
        client = context.client
        client.download_model(urn, dest, args.sub_paths, show_progress_bar=True)

    @classmethod
    def do_upload(cls, context: MetadataContext, args: Namespace):
        client = context.client
        uri = client.upload_artifact(args.storage_prefix, args.path_prefix, args.file, show_progress_bar=True)
        storage_cilent = context.storage_client
        urn = Model.gen_urn(context, storage_cilent.get_name(), args.name)
        entity = Model(
                urn=urn,
                display_name=args.display_name,
                uri=uri,
        )
        client.create_model(entity)
        print(f'Uploaded as {entity}')

    @classmethod
    def do_upload_partial(cls, context: MetadataContext, args: Namespace):
        client = context.client
        model = client.get_model(args.urn)
        client.upload_artifact(model.uri, args.path_prefix, args.file, show_progress_bar=True)

    @classmethod
    def do_describe(cls, context: MetadataContext, args: Namespace, urn: str):
        cilent = context.client
        model = cilent.get_model(urn)
        paths = context.storage_client.list(model.uri, recursive=True)

        if args.output == 'table' or not args.output:
            metas = [context.storage_client.get_meta(path) for path in paths]
            headers = ['path', 'entityTag', 'lastModified', 'contentLength']
            properties = [
                (meta['path'], meta['entityTag'], sizeof_fmt(meta['contentLength']), meta['lastModified'])
                for meta in metas
            ]
            print(format_table(headers, properties, show_headers=not args.no_headers))
            return

        paths = [i[len(model.uri) + 1:] for i in paths]
        files = gen_tree_files(paths) if paths else []
        if args.output and args.output == 'yaml':
            print(dict2yaml(files))
        else:
            if args.jsonpath:
                jsonpath_expression = parse(args.jsonpath)
                for match in jsonpath_expression.find(files):
                    print(match.value)
            else:
                print(dict2json(files))