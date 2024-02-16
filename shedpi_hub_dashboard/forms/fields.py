import json

from django.db.models import JSONField
from django.forms import JSONField as JSONFormField
from django.forms import widgets


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            # Prettify the json
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
        except json.JSONDecodeError:
            return super(PrettyJSONWidget, self).format_value(value)

        # Calculate the size of the contents
        row_lengths = [len(r) for r in value.split("\n")]
        content_width = max(len(row_lengths) + 2, 20)
        content_height = max(max(row_lengths) + 2, 45)

        # Adjust the size of TextArea to fit to content
        self.attrs["rows"] = min(content_width, 60)
        self.attrs["cols"] = min(content_height, 155)

        return value


class PrettyJsonFormField(JSONFormField):
    widget = PrettyJSONWidget


class PrettyJsonField(JSONField):
    def formfield(self, **kwargs):
        defaults = {"form_class": PrettyJsonFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
