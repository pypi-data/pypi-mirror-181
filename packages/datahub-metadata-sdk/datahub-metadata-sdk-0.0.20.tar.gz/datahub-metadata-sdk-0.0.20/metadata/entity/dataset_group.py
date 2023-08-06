# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from metadata.entity.entity import Entity
from metadata.ensure import ensure_entity_name_format, ensure_uri_format, ensure_platform_format, ensure_entity_urn_format

@dataclass
class DatasetGroup(Entity):

    entity_type: str = field(repr=False, init=False, default='container')

    @classmethod
    def gen_urn(cls, context, platform, name, auto_suffix=True):
        ensure_entity_name_format(name)
        env = context.env
        ensure_platform_format(platform)
        qualified_name = cls._gen_qual_name(context, name, auto_suffix=auto_suffix)
        return f'urn:li:{cls.entity_type.lower()}:{platform}:{qualified_name}:{env}'
