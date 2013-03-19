from django.contrib.auth.models import User
from django import forms


class MarkRequiredFieldsMixin(forms.ModelForm):

    def _html_output(self, *args, **kwargs):
        for fieldname, field in self.fields.items():
            if not hasattr(field, "marked_if_required"):
                field.marked_if_required = True
                if field.required and \
                not field.widget.attrs.get('readonly', False) is True:
                    field.label = field.label + "*"
        return super(MarkRequiredFieldsMixin, self)._html_output(*args, **kwargs)


class ModelFormWithReadonlyFields(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelFormWithReadonlyFields, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            Meta = getattr(self, 'Meta', None)
            if Meta:
                readonly_fields = getattr(Meta, 'readonly_fields', [])
                for field in readonly_fields:
                    self.fields[field].widget.attrs['readonly'] = True
                    self.fields[field].help_text = ""

    def clean(self):
        instance = getattr(self, 'instance', None)
        assert not instance is None and not instance.pk is None

        cleaned_data = super(ModelFormWithReadonlyFields, self).clean()

        for field in self.Meta.readonly_fields:
            cleaned_data[field] = getattr(instance, field)
        return cleaned_data


class ProfileForm(ModelFormWithReadonlyFields, MarkRequiredFieldsMixin):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "date_joined",)
        readonly_fields = ("username", "email", "date_joined",)
