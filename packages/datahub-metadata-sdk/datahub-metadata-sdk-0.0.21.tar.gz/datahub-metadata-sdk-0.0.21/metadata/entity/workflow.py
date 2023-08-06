# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Workflow:

    name: str

    id: Optional[str] = field(repr=False, default=None)
    orchestrator: Optional[str] = field(repr=False, default='local')
    description: Optional[str] = field(repr=False, default='')
    properties: Optional[Dict[str, str]] = field(repr=False, default_factory=dict)
    url: Optional[str] = field(repr=False, default='')
    tags: Optional[List[str]] = field(repr=False, default_factory=list)
    owners: Optional[List[str]] = field(repr=False, default_factory=list)

    def __post_init__(self):
        self.id = self.id or uuid.uuid4().hex

WorkFlow = Workflow