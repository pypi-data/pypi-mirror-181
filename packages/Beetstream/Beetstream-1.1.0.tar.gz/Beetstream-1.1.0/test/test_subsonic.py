"""Tests beets beetstream plugin"""

from __future__ import (division, absolute_import, print_function, unicode_literals)
from test import _common
import json
import beetsplug
from beets.library import Item, Album
beetsplug.__path__ = ['./beetsplug', '../beetsplug']  # noqa
from beetsplug import beetstream

class BeetstreamPluginTest(_common.LibTestCase):
    pass