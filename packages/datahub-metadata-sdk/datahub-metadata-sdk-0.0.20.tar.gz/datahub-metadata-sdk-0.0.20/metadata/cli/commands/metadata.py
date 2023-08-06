# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os
import dataclasses
import sys

import coloredlogs
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from metadata.utils.format import format_table, yaml2json, dict2yaml, dict2json
from metadata.context import MetadataContext, get_current_context
from metadata.cli.builtin.dataset import IDataset
from metadata.cli.builtin.dataset_group import IDatasetGroup
from metadata.cli.builtin.model import IModel
from metadata.cli.builtin.model_group import IModelGroup
from metadata.ensure import ensure_true
from metadata.exception import MetadataError
from metadata.cli.commands.login import do_login
from metadata.cli.commands.context import do_context

urllib3.disable_warnings(category=InsecureRequestWarning)
resource_id = None
logger = logging.getLogger(__name__)


class DetectResourceAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        _type = None
        resources = getattr(self, 'resources')
        if '/' in values:
            values, _id = values.split('/', 1)
            global resource_id
            resource_id = _id
        if values in resources:
            _type = values
        else:
            for alias_type, resource in sorted(resources.items(), key=lambda r: getattr(r, 'priority', 0)):
                for alias in getattr(resource, 'candidate_names', []):
                    if values == alias:
                        _type = alias_type
        if _type is None:
            ensure_true(False, 'unknown resource type {values}, choice from {keys}', values=values, keys=list(resources.keys()))
        ensure_true(_type in getattr(self, 'supported_resources'), 'unsupported action for resource type %s', _type)
        setattr(namespace, self.dest, _type)


def get_main_parser(resources, action=None, target=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', help='verbose output')
    parser.add_argument('--quiet', action='store_true', help='quiet output')
    parser.add_argument('--suppress', action='store_true', help='suppress output')
    parser.add_argument('--timeout', action='store', type=int, help='set default http timeout')

    subparsers = parser.add_subparsers(dest='action', help='Sub commands')
    login_parser = subparsers.add_parser('login', help='do login')
    login_parser.add_argument('endpoint', type=str, help='metadata endpoint, eg https://datahub-gms.dp.tech')
    login_parser.add_argument('-n', '--name', action='store', dest='name', type=str)
    login_parser.add_argument('--token', required=False)
    login_parser.add_argument('--project', required=False, default='default')
    login_parser.add_argument('--bohrium-user', required=False)
    login_parser.add_argument('--bohrium-password', required=False)
    login_parser.add_argument('--bohrium-project', required=False)
    login_parser.add_argument('--bohrium-url', required=False)
    login_parser.add_argument('--tiefblue-url', required=False)

    shell_parser = subparsers.add_parser('shell', help='do shell')
    shell_parser.add_argument('-c', '--command', action='store', type=str)
    shell_parser.add_argument('-e', '--statement', action='store', type=str)

    context_parser = subparsers.add_parser('context', help='do context')
    context_parser.add_argument('-s', '--switch', action='store', type=str)
    context_parser.add_argument('-l', '--list', action='store_true')
    context_parser.add_argument('-r', '--remove', action='store', type=str)
    context_parser.add_argument('-c', '--clear', action='store_true')

    if action == 'get' or action is None:
        get_parser = subparsers.add_parser('get', help='Get resources')
        get_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_get')}
        resource_action = get_parser.add_argument('resource', action=DetectResourceAction,
                                                  help='resource type, %s' % list(get_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = get_support_resources
        if action is None:
            get_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            get_parser.add_argument('-s', '--start', action="store", type=int, default=0, help='resource range start')
            get_parser.add_argument('-n', '--limit', action="store", type=int, default=1000, help='limit resources to show')
            get_parser.add_argument('-t', '--tags', action="store", type=str, help='do filter by tags')
            get_parser.add_argument('-f', '--fields', action="store", type=str, help='show only custom fields')
            get_parser.add_argument('-j', '--jsonpath', action="store", type=str, help='trans by jsonpath')
            get_parser.add_argument('-o', '--output', choices=('json', 'yaml'), action='store', dest='output',
                                    help='output format')
            get_parser.add_argument('--no-headers', action='store_true', help='do not show table headers')
            get_parser.add_argument('--no-footer', action='store_true', help='do not show footer info')
            get_parser.add_argument('urn', nargs='?')
            return get_parser

    if action == 'serve' or action is None:
        serve_parser = subparsers.add_parser('serve', help='Serve resources')
        serve_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_serve')}
        resource_action = serve_parser.add_argument('resource', action=DetectResourceAction,
                                                  help='resource type, %s' % list(serve_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = serve_support_resources
        if action is None:
            serve_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            serve_parser.add_argument('-p', '--port', action="store", type=int, default=9527, help='serve port')
            serve_parser.add_argument('--host', action="store", type=str, default='localhost', help='serve host')
            serve_parser.add_argument('urn', nargs='?')
            return serve_parser

    if action == 'delete' or action is None:
        delete_parser = subparsers.add_parser('delete', help='Delete resources')
        delete_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_delete')}
        resource_action = delete_parser.add_argument('resource', action=DetectResourceAction,
                                                     help='resource type, %s' % list(delete_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = delete_support_resources
        if action is None:
            delete_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            delete_parser.add_argument('--hard', action='store_true', help='delete all storage content')
            if target.container_type == 'container':
                delete_parser.add_argument('--cascade', action='store_true', help='delete all sub entities')
            delete_parser.add_argument('urn', nargs='?')
            return delete_parser

    if action == 'describe' or action is None:
        describe_parser = subparsers.add_parser('describe', help='describe resources')
        describe_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_describe')}
        resource_action = describe_parser.add_argument('resource', action=DetectResourceAction,
                                                       help='resource type, %s' % list(
                                                           describe_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = describe_support_resources
        if action is None:
            describe_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            describe_parser.add_argument('urn', nargs='?')
            describe_parser.add_argument('-o', '--output', choices=('json', 'yaml', 'table'), action='store', dest='output',
                                     help='output format')
            describe_parser.add_argument('-j', '--jsonpath', action="store", type=str, help='trans by jsonpath')
            describe_parser.add_argument('--no-headers', action='store_true', help='do not show table headers')
            return describe_parser

    if action == 'download' or action is None:
        download_parser = subparsers.add_parser('download', help='download resources')
        download_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_download')}
        resource_action = download_parser.add_argument('resource', action=DetectResourceAction,
                                                       help='resource type, %s' % list(
                                                           download_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = download_support_resources
        if action is None:
            download_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            download_parser.add_argument('-d', '--dest', type=str, default='.', action='store', help='download dir')
            download_parser.add_argument('-s', '--sub-paths', nargs='+', default=[], help='filter subpaths')
            download_parser.add_argument('urn', nargs='?')
            return download_parser

    if action == 'upload' or action is None:
        upload_parser = subparsers.add_parser('upload', help='upload resources')
        upload_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_upload')}
        resource_action = upload_parser.add_argument('resource', action=DetectResourceAction,
                                                     help='resource type, %s' % list(upload_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = upload_support_resources
        if action is None:
            upload_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            upload_parser.add_argument('-f', '--file', type=str, action='store', required=True, help='file to upload')
            upload_parser.add_argument('--storage-prefix', type=str, action='store', required=False, help='target storage prefix')
            upload_parser.add_argument('--path-prefix', type=str, action='store', required=False, help='target path prefix')
            upload_parser.add_argument('-n', '--name', type=str, action='store', required=True, help='urn name of entity')
            upload_parser.add_argument('-d', '--display-name', type=str, action='store', required=True, help='display name of entity')
            return upload_parser

    if action == 'upload_partial' or action is None:
        upload_partial_parser = subparsers.add_parser('upload_partial', help='upload partial resources')
        upload_partial_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_upload_partial')}
        resource_action = upload_partial_parser.add_argument('resource', action=DetectResourceAction,
                                                     help='resource type, %s' % list(upload_partial_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = upload_partial_support_resources
        if action is None:
            upload_partial_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            upload_partial_parser.add_argument('-f', '--file', type=str, action='store', required=True, help='file to upload')
            upload_partial_parser.add_argument('--urn', type=str, action='store', required=True, help='target urn')
            upload_partial_parser.add_argument('--path-prefix', type=str, action='store', required=False, help='target path prefix')
            return upload_partial_parser

    if action == 'create' or action is None:
        create_parser = subparsers.add_parser('create', help='Create resources')
        create_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_create')}
        resource_action = create_parser.add_argument('resource', action=DetectResourceAction,
                                                     help='resource type, %s' % list(create_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = create_support_resources
        if action is None:
            create_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            create_parser.add_argument('-f', '--from', type=str, action='store', nargs='+', required=True, help='resource define location')
            return create_parser

    if action == 'edit' or action is None:
        edit_parser = subparsers.add_parser('edit', help='edit resources')
        edit_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_edit')}
        resource_action = edit_parser.add_argument('resource', action=DetectResourceAction,
                                                   help='resource type, %s' % list(edit_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = edit_support_resources
        if action is None:
            edit_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            edit_parser.add_argument('-o', '--output', choices=('json', 'yaml'), action='store', dest='output',
                                     help='output format')
            edit_parser.add_argument('urn', nargs='?')
            return edit_parser

    if action == 'update' or action is None:
        update_parser = subparsers.add_parser('update', help='update resources')
        update_support_resources = {name: res for name, res in list(resources.items()) if hasattr(res, 'do_update')}
        resource_action = update_parser.add_argument('resource', action=DetectResourceAction,
                                                     help='resource type, %s' % list(update_support_resources.keys()))
        resource_action.resources = resources
        resource_action.supported_resources = update_support_resources
        if action is None:
            update_parser.add_argument('args', nargs=argparse.REMAINDER)
        else:
            update_parser.add_argument('-f', '--from', action='store')
            update_parser.add_argument('urn', nargs='?')
            return update_parser

    return parser


def get_resource_parser(resources, action, resource):
    parser = get_main_parser(resources, action=action, target=resource)
    group = parser.add_argument_group(resource.name + ' arguments')
    if hasattr(resource, 'options'):
        resource.options(group, action)
    return parser


def main():
    try:
        ensure_logger = logging.getLogger('metadata.ensure')
        ensure_logger.level = logging.CRITICAL
        _main()
    except MetadataError as e:
        logger.error(e)
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
    except KeyboardInterrupt:
        logger.warning('operation silent interrupted !')
        try:
            sys.exit(2)
        except SystemExit:
            os._exit(3)


def _main():
    builtin_resources = [
        IDataset, IDatasetGroup, IModel, IDatasetGroup,
    ]
    resources = {i.name: i for i in builtin_resources}
    parser = get_main_parser(resources)
    main_args = parser.parse_args()

    if main_args.timeout:
        os.environ['defaults.metadata.context.request_timeout'.upper().replace('.', '_')] = str(main_args.timeout)

    if main_args.verbose:
        level = logging.DEBUG
        blevel = level
    elif main_args.quiet:
        level = logging.ERROR
        blevel = level
    elif main_args.suppress:
        level = logging.CRITICAL
        blevel = level
    else:
        level = logging.INFO
        blevel = logging.WARN

    logging.getLogger("requests").setLevel(blevel)
    sys.stderr = sys.stdout
    coloredlogs.install(stream=sys.stdout, level=level,
                        fmt='[%(levelname)s]\t%(asctime)s,%(msecs)03d\t%(name)s\t%(message)s')

    if main_args.action == 'login':
        do_login(main_args)
    elif main_args.action == 'context':
        do_context(main_args)
    elif main_args.action == 'shell':
        if main_args.statement:
            from metadata.utils.ipython import do_eval
            print(do_eval(main_args.statement))
        elif main_args.command:
            from metadata.utils.ipython import do_exec
            do_exec(main_args.command)
        else:
            from metadata.utils.ipython import main as ipython_main
            ipython_main()
    elif main_args.action in (
            'get', 'delete', 'create', 'update', 'edit', 'describe',
            'download', 'upload', 'upload_partial', 'serve'):
        parser = get_resource_parser(resources, main_args.action, resources.get(main_args.resource))
        args = parser.parse_args([main_args.resource] + main_args.args)
        resource = resources.get(main_args.resource)

        context = get_current_context()
        ensure_true(context, 'login required, take `metadata login --help` for more help')

        if main_args.verbose:
            context.debug_requests_on()

        if main_args.action == 'get':
            from jsonpath_ng import parse

            _resource_id = args.urn or resource_id
            logger.debug('before get %s/%s', resource.name, _resource_id)
            output = resource.do_get(context, args, _resource_id)
            if _resource_id:
                ensure_true(output, 'resource %s/%s not found' % (resource.name, _resource_id))
                if args.output == 'yaml':
                    print(dict2yaml(dataclasses.asdict(output)))
                else:
                    if args.jsonpath:
                        jsonpath_expression = parse(args.jsonpath)
                        for match in jsonpath_expression.find(dataclasses.asdict(output)):
                            print(match.value)
                    else:
                        print(dict2json(dataclasses.asdict(output)))
            elif not args.output:
                headers, properties = output
                if properties:
                    print(format_table(headers, properties, show_headers=not args.no_headers))
            elif args.output == 'yaml':
                for index, obj in enumerate(output):
                    if index != '0':
                        print('---')
                    print(dict2yaml(dataclasses.asdict(obj)))
            else:
                if args.jsonpath:
                    jsonpath_expression = parse(args.jsonpath)
                    for obj in output:
                        for match in jsonpath_expression.find(dataclasses.asdict(obj)):
                            print(match.value)
                else:
                    for obj in output:
                        print(dict2json(dataclasses.asdict(obj)))
            logger.debug('after get %s/%s', resource.name, _resource_id)
        elif main_args.action == 'delete':
            _resource_id = args.urn or resource_id
            ensure_true(_resource_id, 'delete resource without id does not support')
            logger.debug('before delete %s/%s', resource.name, _resource_id)
            resource.do_delete(context, args, _resource_id)
            logger.debug('after delete %s/%s', resource.name, _resource_id)
        elif main_args.action == 'describe':
            _resource_id = args.urn or resource_id
            ensure_true(_resource_id, 'describe resource without id does not support')
            logger.debug('before describe %s/%s', resource.name, _resource_id)
            resource.do_describe(context, args, _resource_id)
            logger.debug('after describe %s/%s', resource.name, _resource_id)
        elif main_args.action == 'serve':
            _resource_id = args.urn or resource_id
            ensure_true(_resource_id, 'serve resource without id does not support')
            logger.debug('before serve %s/%s', resource.name, _resource_id)
            resource.do_serve(context, args, _resource_id)
            logger.debug('after serve %s/%s', resource.name, _resource_id)
        elif main_args.action == 'download':
            _resource_id = args.urn or resource_id
            ensure_true(_resource_id, 'download resource without id does not support')
            logger.debug('before download %s/%s', resource.name, _resource_id)
            resource.do_download(context, args, _resource_id)
            logger.debug('after download %s/%s', resource.name, _resource_id)
        elif main_args.action == 'upload':
            logger.debug('before upload %s', resource.name)
            resource.do_upload(context, args)
            logger.debug('after upload %s', resource.name)
        elif main_args.action == 'upload_partial':
            logger.debug('before upload partial %s', resource.name)
            resource.do_upload_partial(context, args)
            logger.debug('after upload patial %s', resource.name)
        elif main_args.action == 'create':
            ensure_true(not resource_id, 'create resource with id does not support')
            logger.debug('before create %s from %s', resource.name, getattr(args, 'from'))
            for _file in getattr(args, 'from'):
                ensure_true(os.path.exists(_file), 'source file `%s` not exists', _file)
                ensure_true(os.path.isfile(_file), 'source file `%s` is not file', _file)
                supported_sources = ('.json', '.dag', '.yaml', '.yml')
                ensure_true(os.path.splitext(_file)[1] in supported_sources,
                            'source file `%s` not recognized, supported ext is %s', _file, supported_sources)
                with open(_file) as f:
                    if os.path.splitext(_file)[1] in ('.json', '.dag'):
                        try:
                            dt = json.loads(f.read())
                        except Exception as e:
                            ensure_true(False, 'source file `%s` is invalid json file, %s', _file, e)
                    elif os.path.splitext(_file)[1] in ('.yaml', '.yml'):
                        try:
                            dt = json.loads(yaml2json(f.read()))
                        except Exception as e:
                            ensure_true(False, 'source file `%s` is invalid yaml file, %s', _file, e)
                resource.do_create(context, args, dt)
            logger.debug('after create %s from %s', resource.name, getattr(args, 'from'))
        elif main_args.action == 'edit':
            _resource_id = args.urn or resource_id
            ensure_true(_resource_id, 'edit resource without id does not support')
            logger.debug('before edit resource %s/%s', resource.name, _resource_id)
            resource.do_edit(context, args, _resource_id)
            logger.debug('after edit resource %s/%s', resource.name, _resource_id)
        elif main_args.action == 'update':
            _resource_id = args.urn or resource_id
            logger.debug('before update resource %s/%s', resource.name, _resource_id)
            _from = getattr(args, 'from')
            dt = None
            if _from:
                ensure_true(os.path.exists(_from), 'source file `%s` not exists', _from)
                ensure_true(os.path.isfile(_from), 'source file `%s` is not file', _from)
                supported_sources = ('.json', '.yaml', '.yml')
                ensure_true(os.path.splitext(_from)[1] in supported_sources,
                            'source file `%s` not recognized, supported ext is %s', _from, supported_sources)
                with open(_from) as f:
                    if os.path.splitext(_from)[1] in ('.json'):
                        try:
                            dt = json.loads(f.read())
                        except Exception as e:
                            ensure_true(False, 'source file `%s` is invalid json file, %s', _from, e)
                    elif os.path.splitext(_from)[1] in ('.yaml', '.yml'):
                        try:
                            dt = json.loads(yaml2json(f.read()))
                        except Exception as e:
                            ensure_true(False, 'source file `%s` is invalid yaml file, %s', _from, e)
            resource.do_update(context, args, _resource_id, dt)
            logger.debug('after update resource %s/%s', resource.name, _resource_id)
        else:
            parser.print_help()
    else:
        parser.print_help()
