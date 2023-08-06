import os
from typing import Type, List, Dict

from django import template
from django.conf import settings
from django.db.models import QuerySet
from django.db.models.fields.files import FieldFile
from django.db.models.functions import Lower
from django.forms.boundfield import BoundField
from django.forms.fields import FileField
from django.template import loader
from django.templatetags.static import static as dstatic
from django.utils.html import escape
from django.utils.safestring import SafeText

from pursuitlib import utils
from pursuitlib.color import is_dark
from pursuitlib.utils import is_null_or_empty

from pursuitlib_django.forms import Form, DEFAULT_FORM_SECTION
from pursuitlib_django.utils import get_verbose_name, get_verbose_name_plural

# Read the Django configuration

VERSION = getattr(settings, "VERSION")
DISPLAY_VERSION = getattr(settings, "DISPLAY_VERSION", VERSION)
BASE_URL = getattr(settings, "BASE_URL")
MEDIA_URL = getattr(settings, "MEDIA_URL")


register = template.Library()


@register.filter
def at(collection, key):
    if key in collection:
        return collection[key]
    elif (isinstance(collection, tuple) or isinstance(collection, list)) and key is int and 0 <= key < len(collection):
        return collection[key]
    return collection[key]


@register.filter
def contains(collection, value) -> bool:
    return value in collection


@register.filter
def concat(value1, value2) -> str:
    return str(value1) + str(value2)


@register.filter
def orderby(query: QuerySet, order_by: str):
    return query.order_by(order_by)


@register.filter
def iorderby(query: QuerySet, order_by: str):
    return query.order_by(Lower(order_by))


@register.simple_tag
def percentage(value: int, total: int, rounding: bool = False):
    if total == 0:
        return "0%"
    elif rounding:
        return str((value * 100 // total)) + "%"
    else: return str((value * 100 / total)) + "%"


@register.filter
def bool_text(value) -> str:
    if value is None:
        return "Inconnu"
    elif value:
        return "Oui"
    else: return "Non"


@register.filter
def as_widget(form_field: BoundField) -> SafeText:
    if isinstance(form_field.field, FileField):
        html = str(form_field.as_widget())
        offset = html.index('<input type="file"')
        has_checkbox = "checkbox" in html

        main = html[offset:]
        checkbox = '</div><div class="form-check m-2">\
                            <input type="checkbox" class="form-check-input" name="' + form_field.name + '-clear" id="' + form_field.name + '-clear_id">\
                            <label class="form-check-label" for="' + form_field.name + '-clear_id">Supprimer</label>'

        return SafeText(main + (checkbox if has_checkbox else ''))
    elif form_field.widget_type == "checkbox":
        return SafeText('<div class="form-check m-2">' + form_field.as_widget() +
                        '<label class="form-check-label" for="' + form_field.id_for_label + '">' + form_field.label + '</label></div>')
    else: return form_field.as_widget()


@register.filter
def unsafe_text(text: str) -> SafeText:
    return SafeText(escape(text).replace("\n", "<br>"))


@register.simple_tag
def static(path: str) -> str:
    return dstatic(path) + "?v=" + VERSION  # Invalidate the client static files cache after every update


@register.filter
def media_url(file: FieldFile) -> str:
    return MEDIA_URL + file.name


@register.filter
def full_url(url: str) -> str:
    return BASE_URL + url


@register.simple_tag
def version() -> str:
    return DISPLAY_VERSION


@register.simple_tag
def versnum() -> str:
    return VERSION


@register.simple_tag
def env(varname: str) -> str:
    return os.getenv(varname)


@register.filter
def alert_type(severity: str) -> str:
    if severity == "debug":
        return "dark"
    elif severity == "info":
        return "info"
    elif severity == "success":
        return "success"
    elif severity == "warning":
        return "warning"
    elif severity == "error":
        return "danger"
    else: return "light"


@register.filter
def not_empty(value) -> bool:
    return not is_null_or_empty(value)


@register.filter
def empty_none(value) -> str:
    if value is None:
        return ""
    else: return value


@register.filter
def filename(path: str) -> str:
    return os.path.basename(path)


@register.filter
def typeof(obj) -> Type:
    return type(obj)


@register.filter
def verbose_name(obj) -> str:
    return get_verbose_name(obj)


@register.filter
def verbose_name_plural(obj) -> str:
    return get_verbose_name_plural(obj)


@register.filter
def is_feminine(obj) -> bool:
    try:
        return type(obj).Gender.feminine
    except AttributeError:
        return False


@register.filter
def genderize(obj, suffix: str = "e") -> str:
    return suffix if is_feminine(obj) else ""


@register.filter
def tostring(obj) -> str:
    return str(obj)


@register.filter()
def liststring(objects) -> str:
    return utils.list_to_string(objects)


@register.filter
def foreground(color: str) -> str:
    return "#FFFFFF" if is_dark(color) else "#000000"


@register.filter
def section_fields(form: Form, section: str) -> List[BoundField]:
    return form.get_section(section)


# Components

@register.simple_tag
def form_section(form: Form, section: str = DEFAULT_FORM_SECTION, padding: bool = True, label: bool = True):
    return loader.get_template("pursuitlib/component/form-section.html").render({"form": form,
                                                                                 "section": section,
                                                                                 "padding": padding,
                                                                                 "display_label": label})


@register.simple_tag
def field(form_field: BoundField, padding: bool = True, label: bool = True):
    return loader.get_template("pursuitlib/component/form-field.html").render({"field": form_field,
                                                                               "padding": padding,
                                                                               "display_label": label})
