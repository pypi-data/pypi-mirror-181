# -*- coding: utf-8 -*-

from collections import namedtuple

ENV_TYPE = namedtuple('ENV_TYPE', ['CORP', 'PROD', 'DEV'])(
    'CORP', 'PROD', 'DEV'
)