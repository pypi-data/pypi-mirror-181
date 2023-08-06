# -*- coding: utf-8 -*-

from typing import Mapping, Any

from metadata.entity.model_group import ModelGroup
from metadata.cli.builtin.entity import IEntity
from metadata.client.client import Client


class IModelGroup(IEntity):

    name = 'model_group'
    candidate_names = ['mdg', 'mg']
    container_type = 'container'

    @classmethod
    def get_one_func(cls, client: Client):
        return client.get_model_group

    @classmethod
    def get_multi_func(cls, client: Client):
        def wraps(*args, **kwargs):
            return [client.get_model_group(urn) for urn in client.get_model_groups_by_facts(*args, **kwargs)]
        return wraps

    @classmethod
    def delete_one_func(cls, client: Client):
        return client.delete_model_group

    @classmethod
    def create_one(cls, client: Client, dt: Mapping[str, Any]):
        model_group = ModelGroup(dt)
        return client.create_model_group(model_group)

    @classmethod
    def update_one(cls, client: Client, dt: Mapping[str, Any]):
        model_group = ModelGroup(**dt)
        return client.update_model_group(model_group)
