# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Union, Dict, Optional, Any, List

from metadata.entity.entity import Entity

@dataclass
class Model(Entity):

    entity_type: str = field(repr=False, init=False, default='mlModel')

    #: Type of Algorithm or MLModel such as whether it is a Naive Bayes classifier, Convolutional Neural Network, etc
    algorithm: Optional[str] = field(repr=False, default=None)
    
    #: Version of the MLModel
    version: Optional[str] = field(repr=False, default=None)

    #: Date when the MLModel was developed
    created_at: Optional[Union[int, datetime]] = field(repr=False, default=None)

    #: Model can join many ModelGroups
    groups: Optional[List[str]] = field(repr=False, default=None)

    #: List of features used for MLModel training
    training_features: Optional[List[str]] = field(repr=False, default=None)

    #: Hyper params for MLModel training
    training_params: Optional[Dict[str, Any]] = field(repr=False, default=None)

    #: Metrics of the MLModel used in training
    training_metrics: Optional[Dict[str, Any]] = field(repr=False, default=None)