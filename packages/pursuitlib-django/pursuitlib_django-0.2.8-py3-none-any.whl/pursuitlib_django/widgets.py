from typing import Type

from django import forms
import django_select2.forms as select2

from django.db.models import Model
from django.utils.translation import get_language


# Generic

class DateInput(forms.TextInput):
    input_type = "date"


# Select2

def set_attrs(attrs):
    attrs['data-token-separators'] = '[",", ";"]'
    attrs['data-theme'] = 'bootstrap-5'
    attrs['data-language'] = get_language()


def hide_search(attrs):
    attrs.setdefault("data-minimum-results-for-search", "Infinity")


class SelectInputWidget(select2.Select2Widget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        set_attrs(attrs)
        hide_search(attrs)
        return attrs


class ModelSelectInputWidget(select2.ModelSelect2Widget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        set_attrs(attrs)
        hide_search(attrs)
        return attrs


class ListInputWidget(select2.Select2MultipleWidget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        set_attrs(attrs)
        return attrs


class ModelListInputWidget(select2.ModelSelect2MultipleWidget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        set_attrs(attrs)
        return attrs


class TagInputWidget(select2.ModelSelect2TagWidget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        set_attrs(attrs)
        return attrs

    def value_from_datadict(self, data, files, name):
        vtype = self.get_value_type()
        values = super().value_from_datadict(data, files, name)

        for i in range(len(values)):
            if not values[i].isdigit():  # If this is a newly created object
                if self.use_lowercase_names():
                    values[i] = values[i].lower()
                try:
                    values[i] = self.queryset.get(name__iexact=values[i]).pk  # If the object already exists, don't create a new one
                except vtype.DoesNotExist:
                    values[i] = self.queryset.create(name=values[i]).pk

        return values

    def get_value_type(self) -> Type[Model]:
        raise NotImplemented()

    def use_lowercase_names(self) -> bool:
        return True


class SuggestTagInputWidget(TagInputWidget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs["data-minimum-input-length"] = 0
        return attrs
