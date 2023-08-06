# -*- encoding: utf-8 -*-

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from metadata.ensure import ensure_entity_name_format, ensure_uri_format, ensure_platform_format, ensure_entity_urn_format

@dataclass
class BaseEntity:

    urn: str
    display_name: str = field(repr=False, default='')
    description: str = field(repr=False, default='')
    tags: List[str] = field(repr=False, default_factory=list)
    properties: Dict[str, str] = field(repr=False, default_factory=dict)
    owners: Optional[List[str]] = field(repr=False, default=None)

    entity_type: str = field(repr=False, init=False, default='unknown')

    def __post_init__(self):
        ensure_entity_urn_format(self.urn)

    @classmethod
    def _gen_qual_name(cls, context, name, auto_suffix):
        project = context.project
        suffix = ('-' + uuid.uuid4().hex[:6]) if auto_suffix else ''
        qualified_name = f'{project}.{name}{suffix}'
        return qualified_name
    
    @classmethod
    def gen_urn(cls, context, platform, name, auto_suffix=True):
        ensure_entity_name_format(name)
        env = context.env
        ensure_platform_format(platform)
        qualified_name = cls._gen_qual_name(context, name, auto_suffix=auto_suffix)
        return f'urn:li:{cls.entity_type}:(urn:li:dataPlatform:{platform},{qualified_name},{env})'

@dataclass
class Entity(BaseEntity):
    
    uri: str = field(repr=False, default='')

    def __post_init__(self):
        ensure_uri_format(self.uri)