from django.forms import ModelForm, TextInput, JSONField
from .models import Curriculum


class ListAsStringField(JSONField):
    def to_python(self, value):
        if not value:
            return []
        return value.split(",")

    def prepare_value(self, value):
        return ",".join(value)


class CurricilumForm(ModelForm):
    class Meta:
        model = Curriculum
        fields = ["semester_number", "profile", "program_name", "exam", "test"]
        labels = {
            "semester_number": ("Семестр"),
        }
        help_texts = {
            "semester_number": ("Введите номер семестра."),
        }
        field_classes = {"semester_number": ListAsStringField}
        widgets = {"semester_number": TextInput}
