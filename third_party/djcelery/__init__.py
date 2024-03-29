"""Django Celery Integration."""
import os


VERSION = (2, 2, 7)

__version__ = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__author__ = "Ask Solem"
__contact__ = "ask@celeryproject.org"
__homepage__ = "http://celeryproject.org"
__docformat__ = "restructuredtext"
__license__ = "BSD (3 clause)"


def setup_loader():
    os.environ.setdefault("CELERY_LOADER", "djcelery.loaders.DjangoLoader")

# Importing this module enables the Celery Django loader.
setup_loader()
