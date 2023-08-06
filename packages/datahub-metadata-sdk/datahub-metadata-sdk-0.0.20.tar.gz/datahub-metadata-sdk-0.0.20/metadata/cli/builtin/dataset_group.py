# -*- coding: utf-8 -*-

from typing import Mapping, Any

from metadata.entity.dataset_group import DatasetGroup
from metadata.cli.builtin.entity import IEntity
from metadata.client.client import Client


class IDatasetGroup(IEntity):

    name = 'dataset_group'
    candidate_names = ['dsg', 'dg']
    container_type = 'container'

    @classmethod
    def get_one_func(cls, client: Client):
        return client.get_dataset_group

    @classmethod
    def get_multi_func(cls, client: Client):
        def wraps(*args, **kwargs):
            return [client.get_dataset_group(urn) for urn in client.get_dataset_groups_by_facts(*args, **kwargs)]
        return wraps

    @classmethod
    def delete_one_func(cls, client: Client):
        return client.delete_dataset_group

    @classmethod
    def create_one(cls, client: Client, dt: Mapping[str, Any]):
        dataset_group = DatasetGroup(dt)
        return client.create_dataset_group(dataset_group)

    @classmethod
    def update_one(cls, client: Client, dt: Mapping[str, Any]):
        dataset_group = DatasetGroup(**dt)
        return client.update_dataset_group(dataset_group)
