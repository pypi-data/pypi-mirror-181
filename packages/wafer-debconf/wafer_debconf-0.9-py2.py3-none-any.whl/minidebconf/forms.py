from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as _p

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from minidebconf.models import Diet, Registration, ShirtSize


def register_form_factory():
    form_fields = [
        'full_name', 'involvement', 'gender', 'country', 'city_state', 'days']
    if Diet.objects.exists():
        form_fields.append('diet')
    if ShirtSize.objects.exists():
        form_fields.append('shirt_size')


    class RegisterForm(forms.ModelForm):
        full_name = forms.CharField(max_length=256, label=_('Full name'))
        class Meta:
            model = Registration
            fields = form_fields
            widgets = {
                'days': forms.CheckboxSelectMultiple(),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["full_name"].initial = self.instance.full_name
            self.helper = FormHelper()

            if self.instance.id:
                submit = _p("conference", "Update registration")
            else:
                submit = _p("conference", "Register")
            self.helper.add_input(Submit("submit", submit))


        def save(self):
            super().save()
            name = self.cleaned_data['full_name'].split()
            user = self.instance.user
            user.first_name = name[0]
            user.last_name = " ".join(name[1:])
            user.save()
    return RegisterForm
