import json

from django.forms import JSONField as JSONFormField
from django.forms import widgets


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        # Prettify the json
        value = json.dumps(json.loads(value), indent=2, sort_keys=True)

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
