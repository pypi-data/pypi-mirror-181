# -*- coding: utf-8 -*-

import os
import tempfile
from subprocess import call

from metadata.exception import MetadataError


def system_edit(data):
    editor = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".tmp") as tf:
        tf.write(data)
        tf.flush()
        if call([editor, tf.name]):
            raise MetadataError('cancel')
        file = open(tf.name, 'a+')
        file.seek(0)
        temp = file.read()
        return temp
