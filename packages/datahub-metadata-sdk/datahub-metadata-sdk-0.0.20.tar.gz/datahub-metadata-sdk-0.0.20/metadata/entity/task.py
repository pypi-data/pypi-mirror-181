# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from datahub.utilities.urns.data_job_urn import DataJobUrn
from datahub.utilities.urns.data_flow_urn import DataFlowUrn

@dataclass
class Task:

    name: str
    workflow: Union[str, DataFlowUrn]

    id: Optional[str] = field(repr=False, default=None)
    tags: Optional[List[str]] = field(repr=False, default_factory=list)
    properties: Optional[Dict[str, str]] = field(repr=False, default_factory=dict)
    description: Optional[str] = field(repr=False, default_factory=str)
    url: Optional[str] = field(repr=False, default_factory=str)
    upstream_urns: Optional[List[Union[str, DataJobUrn]]] = field(repr=False, default_factory=list)
    owners: Optional[List[str]] = field(repr=False, default_factory=list)

    def __post_init__(self):
        self.id = self.id or uuid.uuid4().hex
        self.workflow = str(self.workflow)
        self.upstream_urns = [str(s) for s in self.upstream_urns or []]