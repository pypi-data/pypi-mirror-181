# -*- coding: utf-8 -*-

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Optional, List

from metadata.entity.entity import BaseEntity

@dataclass
class ModelGroup(BaseEntity):

    version: str = field(repr=False, default=None)
    created_at: int = field(repr=False, default=None)

    entity_type: str = field(repr=False, init=False, default='mlModelGroup')