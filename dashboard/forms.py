from django.forms import ModelForm
from core.models import OpenSpace


class OpenSpaceForm(ModelForm):
    class Meta:
        model = OpenSpace
        fields = '__all__'
