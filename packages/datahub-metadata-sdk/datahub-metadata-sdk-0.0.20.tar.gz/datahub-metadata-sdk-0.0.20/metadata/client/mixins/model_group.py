# -*- encoding: utf-8 -*-

import os.path
import logging
from typing import List
from datetime import datetime

from datahub.emitter.mce_builder import make_tag_urn, make_user_urn
from datahub.metadata.schema_classes import MLModelGroupPropertiesClass, VersionTagClass

from metadata.utils.page import get_all
from metadata.exception import MetadataAssertionError
from metadata.ensure import ensure_timestamp
from metadata.entity.model_group import ModelGroup

logger = logging.getLogger(__name__)


class ModelGroupMixin:

    def create_model_group(self, model_group: ModelGroup, upsert: bool=True):
        model_group_properties = MLModelGroupPropertiesClass(
            customProperties=model_group.properties,
            version=VersionTagClass(model_group.version) if model_group.version else None,
            description=model_group.description,
            createdAt=ensure_timestamp(model_group.created_at) if model_group.created_at else int(datetime.now().timestamp() * 1000),
        )
        global_tags = self._get_tags_aspect(model_group.tags)
        owner_aspect = self._get_ownership_aspect(model_group.owners or [self.context.user_email])
        self._emit_aspects(ModelGroup.entity_type, model_group.urn, [model_group_properties, global_tags, owner_aspect])
        return model_group.urn

    def update_model_group(self, model_group: ModelGroup):
        return self.create_model_group(model_group, upsert=True)

    def get_model_group(self, urn: str):
        if not self.check_entity_exists(urn):
            return
        r = self._query_graphql(ModelGroup.entity_type, urn=urn)['data'][ModelGroup.entity_type]
        properties = r.get('properties', {})
        custom_properties = {e['key']: e['value'] for e in properties.get('customProperties', {})}
        display_name = custom_properties.pop('display_name', r['name'])
        tags = [t['tag']['urn'].split(':', maxsplit=3)[-1] for t in r.get('tags', {}).get('tags', [])]
        model_group = ModelGroup(
            urn=urn,
            tags=tags,
            display_name=display_name,
            description=properties.get('description', r.get('description', '')),
            owners=[o['owner']['urn'].split(':', maxsplit=3)[-1] for o in r.get('ownership', {}).get('owners', [])],
            properties=custom_properties,
            created_at=properties.get('createdAt'),
            version=properties.get('version'),
        )
        return model_group

    def delete_model_group(self, urn: str, cascade=False, soft=True):
        if cascade:
            for urn in get_all(self.get_models_by_group, urn):
                self.delete_model(urn, soft=soft)
        return self._delete_entity(urn)

    def add_model_into_group(self, urn: str, group_urn: str, sync_wait=True):
        model = self.get_model(urn)
        if model and group_urn not in model.groups:
            model.groups.append(group_urn)
            self.update_model(model)
            if sync_wait:
                self._sync_check(f'add {urn} into {group_urn}', lambda : urn in self.get_models_by_group(group_urn))

    def remove_model_from_group(self, urn: str, group_urn: str, sync_wait=True):
        model = self.get_model(urn)
        if model and group_urn in model.groups:
            model.groups.remove(group_urn)
            self.update_model(model)
            if sync_wait:
                self._sync_check(f'remove {urn} from {group_urn}', lambda : urn not in self.get_models_by_group(group_urn))

    def get_models_by_group(self, group_urn: str, *, start=0, count=1000, return_page_info=False):
        if not self.check_entity_exists(group_urn):
            raise MetadataAssertionError(f'ModelGroup(urn={group_urn}) does not exists')
        r = self._query_graphql('mlModelGroup.relationships', urn=group_urn, types='MemberOf', direction='INCOMING', start=start, count=count)
        rr = r['data']['mlModelGroup']['relationships']
        page_info = {
            'start': rr.get('start'),
            'count': rr.get('count'),
            'total': rr.get('total'),
        }
        rs = [i['entity']['urn'] for i in rr['relationships']]
        return (rs, page_info) if return_page_info else rs

    def get_model_groups_by_facts(self, *, owner: str=None, tags: List[str]=None, search: str='', start=0, count=10000, return_page_info=False):
        facts = []
        if tags:
            for tag in tags:
                facts.append(('tags', [make_tag_urn(tag)], False, 'CONTAIN'))
        if owner:
            facts.append(('owners', [make_user_urn(self.context.user_email if owner == 'me' else owner)], False, 'CONTAIN'))
        return self._get_entities_by_facts('MLMODEL_GROUP', facts, search=search, start=start, count=count)
