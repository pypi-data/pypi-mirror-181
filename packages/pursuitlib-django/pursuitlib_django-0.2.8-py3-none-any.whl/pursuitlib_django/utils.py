import os
from typing import Optional
from typing import Type

from django.conf import settings
from django.db import ProgrammingError
from django.db.models import Model, FileField

# Read the Django configuration
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")


def get_media_path(media: FileField) -> Optional[str]:
    return os.path.join(MEDIA_ROOT, media.name) if media else None


def get_model_ctype_name(model: Type[Model]) -> str:
    return model.__name__.lower()


# noinspection PyProtectedMember
def get_verbose_name(obj) -> str:
    try:
        return obj._meta.verbose_name
    except AttributeError:
        return type(obj).__name__


# noinspection PyProtectedMember
def get_verbose_name_plural(obj) -> str:
    try:
        return obj._meta.verbose_name_plural
    except AttributeError:
        return get_verbose_name(obj) + "s"


def safemap(function, input_set) -> map:  # Used to create maps without throwing an error when the database has not been yet initialized
    try:
        return map(function, input_set)
    except ProgrammingError:  # If the database has not been yet initialized, return an empty list, this souldn't matter anyway
        return map(lambda x: x, [])
