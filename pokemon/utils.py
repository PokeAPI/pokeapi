from __future__ import unicode_literals
import time


def unique_filename(instance, old_filename):
    filename = str(time.time()) + '.png'
    return 'img/' + filename
