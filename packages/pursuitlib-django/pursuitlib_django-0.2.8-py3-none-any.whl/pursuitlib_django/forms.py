from typing import List, Optional, Dict

import django.forms as dforms
from django.contrib import messages
from django.forms import BoundField
from django.forms.widgets import CheckboxInput, TextInput, Select
from django.http import HttpRequest
from django.utils.safestring import SafeText
from django_select2.forms import Select2Mixin
from pursuitlib.utils import is_null_or_empty, get_oneline_string

DEFAULT_LIST_HTML = "<ul><li>&nbsp;</li></ul>"
DEFAULT_FORM_SECTION = "main"


class Form(dforms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self:
            self.transform_field(field)
        for field in self.get_text_list_fields():
            if field not in self.initial:
                self.initial.setdefault(field, DEFAULT_LIST_HTML)
            elif is_null_or_empty(self.initial[field]):
                self.initial[field] = DEFAULT_LIST_HTML

    def order_fields(self, field_order):
        super().order_fields(field_order)
        self.add_dynamic_fields()

    def add_dynamic_fields(self):
        pass

    def transform_field(self, field: BoundField):
        field.section = DEFAULT_FORM_SECTION
        for sname, sfields in self.get_sections().items():
            if field.name in sfields:
                field.section = sname
                break

        field.visible = self.is_visible_by_default(field)

        if field.widget_type == "checkbox":
            field.display_label = False
            field.display_icon = False
        elif field.widget_type == "ckeditor" or field.widget_type == "ckeditoruploading":
            field.display_label = True
            field.display_icon = False
        else:
            field.display_label = True
            field.display_icon = True

        field.icon = self.get_icon_for_field(field)

        widget = field.field.widget

        if isinstance(widget, CheckboxInput):
            widget.attrs["class"] = "form-check-input"
        else:
            if isinstance(widget, TextInput):
                widget.attrs["autocomplete"] = "off"

            if isinstance(widget, Select):
                widget.attrs["class"] = "form-select"
            else:
                widget.attrs["class"] = "form-control"

            if isinstance(widget, Select2Mixin):
                # noinspection PyUnresolvedReferences
                widget.attrs["data-placeholder"] = self.get_field_placeholder(field)
            else: widget.attrs["placeholder"] = self.get_field_placeholder(field)

    def full_clean(self):
        super().full_clean()
        for field in self.get_text_list_fields():
            if get_oneline_string(self.cleaned_data[field]) == DEFAULT_LIST_HTML:
                self.cleaned_data[field] = ""
                if hasattr(self.instance, field):
                    setattr(self.instance, field, "")

    def get_title(self) -> str:
        return "Formulaire"

    def get_page_title(self) -> str:
        return self.get_title()

    def get_header(self) -> Optional[str or SafeText]:
        return None

    def get_submit_text(self) -> str:
        return "Envoyer"

    def get_sections(self) -> Dict[str, List[str]]:
        return {}

    def get_section(self, section: str) -> List[BoundField]:
        fields = []
        for field in self:
            if field.section == section:
                fields.append(field)
        return fields

    def is_visible_by_default(self, field: BoundField) -> bool:
        return True

    def get_icon_for_field(self, field: BoundField) -> str:
        return "fas fa-arrow-right"

    def get_field_placeholder(self, field: BoundField) -> str:
        return field.label + " ..."

    def get_text_list_fields(self) -> List[str]:
        return []


class ModelForm(Form, dforms.ModelForm):
    pass


def display_form_errors(request: HttpRequest, form: Form):
    errors = form.errors
    for field in errors:
        messages.add_message(request, messages.ERROR, errors[field].as_text()[2:].replace("* ", ""))
