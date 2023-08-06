import os
from typing import List


def delete_media(model, fields: List[str]):
    for field in fields:
        value = getattr(model, field)

        if value:
            if os.path.isfile(value.path):
                os.remove(value.path)


def update_media(model, fields: List[str]):
    if not model.pk:
        return False

    try:
        old_model = type(model).objects.get(pk=model.pk)

        for field in fields:
            value = getattr(model, field)
            old_value = getattr(old_model, field)

            if old_value != value:
                if old_value and os.path.isfile(old_value.path):
                    os.remove(old_value.path)
    except type(model).DoesNotExist:
        return False
