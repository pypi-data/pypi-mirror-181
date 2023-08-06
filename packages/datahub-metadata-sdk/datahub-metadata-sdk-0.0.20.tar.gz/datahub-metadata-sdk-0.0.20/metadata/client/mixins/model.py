# -*- encoding: utf-8 -*-

import os.path
import copy
import logging
from typing import List, Optional
from datetime import datetime

from datahub.emitter.mce_builder import make_tag_urn, make_user_urn
from datahub.metadata.schema_classes import (
    MLModelPropertiesClass, MLMetricClass, VersionTagClass, MLHyperParamClass,
)

from metadata.ensure import ensure_timestamp, ensure_true
from metadata.entity.model import Model

logger = logging.getLogger(__name__)


class ModelMixin:

    def create_model(self,  model: Model, upsert=True):
        properties = copy.deepcopy(model.properties)
        properties['display_name'] = model.display_name
        properties['uri'] = model.uri
        model_properties = MLModelPropertiesClass(
            customProperties=properties,
            description=model.description,
            type=model.algorithm,
            version=VersionTagClass(model.version) if model.version else None,
            date=ensure_timestamp(model.created_at) if model.created_at else int(datetime.now().timestamp() * 1000),
            groups=model.groups,
            trainingMetrics=[
                MLMetricClass(name=key, vlaue=str(value) if value else None) for key, value in (model.training_metrics or {}).items()
            ],
            hyperParams=[
                MLHyperParamClass(name=key, vlaue=str(value) if value else None) for key, value in (model.training_params or {}).items()
            ],
            mlFeatures=model.training_features,
        )
        global_tags = self._get_tags_aspect(model.tags)
        owner_aspect = self._get_ownership_aspect(model.owners or [self.context.user_email])
        self._emit_aspects(Model.entity_type, model.urn, [model_properties, global_tags, owner_aspect])
        return model.urn

    def update_model(self, model: Model):
        return self.create_model(model, upsert=True)

    def get_model(self, urn: str):
        if not self.check_entity_exists(urn):
            return
        r = self._query_graphql(Model.entity_type, urn=urn)['data']['mlModel']
        properties = r.get('properties', {})
        custom_properties = {e['key']: e['value'] for e in properties.get('customProperties', {})}
        display_name = custom_properties.pop('display_name', r['name'])
        uri = custom_properties.pop('uri', None)
        tags = [t['tag']['urn'].split(':', maxsplit=3)[-1] for t in r.get('tags', {}).get('tags', [])]
        model = Model(
            urn=urn,
            display_name=display_name,
            uri=uri,
            tags=tags,
            description=properties.get('description', r.get('description', '')),
            properties=custom_properties,
            algorithm=properties.get('type'),
            created_at=properties.get('date'),
            version=properties.get('version'),
            owners=[o['owner']['urn'].split(':', maxsplit=3)[-1] for o in r.get('ownership', {}).get('owners', [])],
            groups=[group['urn'] for group in properties.get('groups', [])],
            training_metrics={item['name']: item['value'] for item in properties.get('trainingMetrics', [])},
            training_params={item['name']: item['value'] for item in properties.get('hyperParams', [])},
            training_features=properties.get('mlFeatures', []),
        )
        return model

    def delete_model(self, urn: str, soft=True):
        model = self.get_model(urn)
        if not model:
            return
        if not soft:
            self.delete_artifact(model.uri)
        self._delete_entity(urn, soft=soft)

    def get_models_by_facts(self, *, owner: str=None, group: str=None, tags: List[str]=None, search: str="", start=0, count=10000):
        facts = []
        # TODO group
        if tags:
            for tag in tags:
                facts.append(('tags', [make_tag_urn(tag)], False, 'CONTAIN'))
        if owner:
            facts.append(('owners', [make_user_urn(self.context.user_email if owner == 'me' else owner)], False, 'CONTAIN'))
        return self._get_entities_by_facts(Model.entity_type, facts, search=search, start=start, count=count)

    def download_model(self, urn: str, dest: str, sub_paths: Optional[List[str]], show_progress_bar: str=False):
        model = self.get_model(urn)
        storage_client = self.context.storage_client
        ensure_true(storage_client, 'Storage Client required for context')
        files = storage_client.list(model.uri, recursive=True)
        sub_paths = tuple(sub_paths) if sub_paths else None
        for file in files:
            rfile = file[len(model.uri)+1:]
            if sub_paths and not rfile.startswith(sub_paths):
                continue
            target = os.path.abspath(os.path.join(dest, rfile))
            storage_client.download(file, target, show_progress_bar=show_progress_bar)
