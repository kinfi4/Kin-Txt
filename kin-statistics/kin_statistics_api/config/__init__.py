from __future__ import absolute_import, unicode_literals
import warnings


def warn(*args, **kwargs):
    pass


warnings.warn = warn


__all__ = ['celery_app']
