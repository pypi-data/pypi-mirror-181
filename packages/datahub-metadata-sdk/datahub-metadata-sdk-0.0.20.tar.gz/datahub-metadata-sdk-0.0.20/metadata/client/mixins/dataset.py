# -*- encoding: utf-8 -*-

import copy
import glob
import os.path
import logging
from typing import List, Optional

from datahub.emitter.mce_builder import make_tag_urn, make_user_urn
from datahub.metadata.schema_classes import DatasetPropertiesClass, ContainerClass, ChangeTypeClass

from metadata.ensure import ensure_type, ensure_true
from metadata.entity.dataset import Dataset
from datahub.metadata.com.linkedin.pegasus2avro.dataset import DatasetLineageTypeClass, UpstreamClass, UpstreamLineage

logger = logging.getLogger(__name__)


class DatasetMixin:

    def create_dataset(self,  dataset: Dataset, upsert=True):
        ensure_type(dataset, Dataset)
        properties = copy.deepcopy(dataset.properties)
        properties['uri'] = dataset.uri
        dataset_properties = DatasetPropertiesClass(
            name=dataset.display_name,
            customProperties=properties,
            description=dataset.description,
        )
        global_tags = self._get_tags_aspect(dataset.tags)
        owner_aspect = self._get_ownership_aspect(dataset.owners or [self.context.user_email])
        container_aspect = ContainerClass(
            dataset.group
        ) if dataset.group else None
        self._emit_aspects(Dataset.entity_type, dataset.urn, filter(None, [dataset_properties, global_tags, owner_aspect, container_aspect]))
        return dataset.urn

    def update_dataset(self, dataset: Dataset):
        return self.create_dataset(dataset, upsert=True)

    def get_dataset(self, urn: str):
        if not self.check_entity_exists(urn):
            return
        r = self._query_graphql(Dataset.entity_type, urn=urn)['data']['dataset']
        properties = r.get('properties', {})
        custom_properties = {e['key']: e['value'] for e in properties.get('customProperties', {})}
        display_name = properties.get('name', r.get('name'))
        uri = custom_properties.pop('uri', None)
        tags = [t['tag']['urn'].split(':', maxsplit=3)[-1] for t in r.get('tags', {}).get('tags', [])]
        dataset = Dataset(
            urn=urn,
            display_name=display_name,
            uri=uri,
            tags=tags,
            description=properties.get('description', r.get('description', '')),
            properties=custom_properties,
            owners=[o['owner']['urn'].split(':', maxsplit=3)[-1] for o in r.get('ownership', {}).get('owners', [])],
            group=r.get('container', {}).get('urn'),
        )
        return dataset

    def delete_dataset(self, urn: str, soft=True):
        dataset = self.get_dataset(urn)
        if not dataset:
            return
        if not soft:
            self.delete_artifact(dataset.uri)
        self._delete_entity(urn, soft=soft)

    def get_datasets_by_facts(self, *, owner: str=None, group: str=None, tags: List[str]=None, search: str='', start=0, count=1000):
        facts = []
        if group:
            facts.append(('container', [group], False, 'EQUAL'))
        if tags:
            for tag in tags:
                facts.append(('tags', [make_tag_urn(tag)], False, 'CONTAIN'))
        if owner:
            facts.append(('owners', [make_user_urn(self.context.user_email if owner == 'me' else owner), False, 'CONTAIN']))
        return self._get_entities_by_facts(Dataset.entity_type, facts, search=search, start=start, count=count)

    def download_dataset(self, urn: str, dest: str, sub_paths: Optional[List[str]]=None, show_progress_bar: str=False, progress_callback=None):
        dataset = self.get_dataset(urn)
        storage_client = self.context.storage_client
        ensure_true(storage_client, 'Storage Client required for context')
        files = storage_client.list(dataset.uri, recursive=True)
        sub_paths = tuple(sub_paths) if sub_paths else None
        for file in files:
            rfile = file[len(dataset.uri)+1:]
            if sub_paths and not rfile.startswith(sub_paths):
                continue
            target = os.path.abspath(os.path.join(dest, rfile))
            storage_client.download(file, target, show_progress_bar=show_progress_bar, progress_callback=progress_callback)

    def set_upstream(self, dataset: Dataset, upstream_list: List[Dataset]):
        upstreams = []
        for _dataset in upstream_list:
            upstream_table = UpstreamClass(
                dataset=_dataset.urn,
                type=DatasetLineageTypeClass.TRANSFORMED)
            upstreams.append(upstream_table)
        upstream_lineage = UpstreamLineage(upstreams=upstreams)
        self._emit_aspects(Dataset.entity_type, dataset.urn, upstream_lineage)
