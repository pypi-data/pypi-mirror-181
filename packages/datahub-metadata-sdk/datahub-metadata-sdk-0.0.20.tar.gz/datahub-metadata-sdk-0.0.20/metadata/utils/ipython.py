# -*- encoding: utf-8 -*-

import logging
from traitlets.config import get_config

from metadata.context import MetadataContext, get_current_context
from metadata.entity.dataset import Dataset # noqa
from metadata.entity.dataset_group import DatasetGroup # noqa
from metadata.entity.model import Model # noqa
from metadata.entity.model_group import ModelGroup # noqa


logger = logging.getLogger(__name__)


def do_exec(command):
    with get_current_context() as context:
        sc = context.storage_client
        client = context.client
        return exec(command, globals(), locals())

def do_eval(statement):
    with get_current_context() as context:
        sc = context.storage_client
        client = context.client
        return eval(statement, globals(), locals())

def main():
    import IPython
    context = get_current_context()
    context.start()
    sc = context.storage_client
    client = context.client
    c = get_config()
    c.InteractiveShellEmbed.colors = "Linux"
    IPython.embed(config=c)