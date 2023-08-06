# -*- encoding: utf-8 -*-

import logging
from typing import List

from datahub.emitter.mce_builder import make_tag_urn, make_user_urn
from datahub.metadata.schema_classes import ContainerPropertiesClass

from metadata.utils.page import get_all
from metadata.exception import MetadataAssertionError
from metadata.entity.dataset_group import DatasetGroup

logger = logging.getLogger(__name__)


class DatasetGroupMixin:

    def create_dataset_group(self,  dataset_group: DatasetGroup, upsert: bool = True):
        dataset_group_properties = ContainerPropertiesClass(
            customProperties=dataset_group.properties,
            name=dataset_group.display_name,
            description=dataset_group.description
        )
        global_tags = self._get_tags_aspect(dataset_group.tags)
        owner_aspect = self._get_ownership_aspect(dataset_group.owners or [self.context.user_email])
        self._emit_aspects(DatasetGroup.entity_type, dataset_group.urn, [dataset_group_properties, global_tags, owner_aspect])
        return dataset_group.urn

    def update_dataset_group(self, dataset_group: DatasetGroup):
        return self.create_dataset_group(dataset_group, upsert=True)

    def get_dataset_group(self, urn: str):
        if not self.check_entity_exists(urn):
            return
        r = self._query_graphql(DatasetGroup.entity_type, urn=urn)['data'][DatasetGroup.entity_type]
        properties = r.get('properties', {})
        custom_properties = {e['key']: e['value'] for e in properties.get('customProperties', {})}
        display_name = properties.get('name', r.get('name'))
        tags = [t['tag']['urn'].split(':', maxsplit=3)[-1] for t in r.get('tags', {}).get('tags', [])]
        dataset_group = DatasetGroup(
            urn=urn,
            tags=tags,
            display_name=display_name,
            description=properties.get('description', r.get('description', '')),
            owners=[o['owner']['urn'].split(':', maxsplit=3)[-1] for o in r.get('ownership', {}).get('owners', [])],
            properties=custom_properties,
        )
        return dataset_group

    def delete_dataset_group(self, urn: str, cascade=False, soft=True):
        if cascade:
            for urn in get_all(self.get_datasets_by_group, urn):
                self.delete_dataset(urn, soft=soft)
        self._delete_entity(urn, soft=soft)

    def change_dataset_group(self, urn: str, group_urn: str, sync_wait=True):
        dataset = self.get_dataset(urn)
        if dataset and group_urn != dataset.group:
            dataset.group = group_urn
            self.update_dataset(dataset)
            if sync_wait:
                self._sync_check(f'change {urn} group to {group_urn}', lambda : urn not in self.get_datasets_by_group(group_urn))

    def get_datasets_by_group(self, group_urn: str, *, start=0, count=1000, return_page_info=False):
        if not self.check_entity_exists(group_urn):
            raise MetadataAssertionError(f'DatasetGroup(urn={group_urn}) does not exists')
        r = self._query_graphql('container.relationships', urn=group_urn, types='IsPartOf', direction='INCOMING', start=start, count=count)
        rr = r['data']['container']['relationships']
        rs = [i['entity']['urn'] for i in rr['relationships']]
        page_info = {
            'start': rr.get('start'),
            'count': rr.get('count'),
            'total': rr.get('total'),
        }
        return (rs, page_info) if return_page_info else rs

    def get_dataset_groups_by_facts(self, *, owner: str=None, tags: List[str]=None, search: str='', start=0, count=1000, return_page_info=False):
        facts = []
        if tags:
            for tag in tags:
                facts.append(('tags', [make_tag_urn(tag)], False, 'CONTAIN'))
        if owner:
            facts.append(('owners', [make_user_urn(self.context.user_email if owner == 'me' else owner)], False, 'CONTAIN'))
        return self._get_entities_by_facts(DatasetGroup.entity_type, facts, search=search, start=start, count=count, return_page_info=return_page_info)
