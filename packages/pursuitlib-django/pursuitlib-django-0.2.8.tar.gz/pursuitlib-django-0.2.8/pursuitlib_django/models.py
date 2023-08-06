from django.conf import settings
from django.db.models.fields.files import FileField, ImageField
from django.forms import forms

# Read the Django configuration
MAX_UPLOAD_SIZE = getattr(settings, "MAX_UPLOAD_SIZE", 5)  # The default max upload size is 5 MiB


MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE * 1024 * 1024  # Convert from MiB to bytes
UPLOAD_ERROR_MSG = f"Le fichier téléversé est trop grand. Il doit avoir une taille inférieure à {MAX_UPLOAD_SIZE} Mo"


class FileUploadField(FileField):
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        if data.file.size > MAX_UPLOAD_SIZE_BYTES:
            raise forms.ValidationError(UPLOAD_ERROR_MSG)
        return data


class ImageUploadField(ImageField):
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        if data.file.size > MAX_UPLOAD_SIZE_BYTES:
            raise forms.ValidationError(UPLOAD_ERROR_MSG)
        return data
