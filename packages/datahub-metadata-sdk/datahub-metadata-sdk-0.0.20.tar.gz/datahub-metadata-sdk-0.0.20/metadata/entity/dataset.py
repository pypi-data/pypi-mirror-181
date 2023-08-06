# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass, field

from metadata.entity.entity import Entity

@dataclass
class Dataset(Entity):

    entity_type: str = field(repr=False, init=False, default='dataset')
    group: Optional[str] = field(repr=False, default=None)