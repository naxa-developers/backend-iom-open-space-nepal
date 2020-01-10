from django.forms import ModelForm
from core.models import OpenSpace, AvailableFacility, QuestionList


class OpenSpaceForm(ModelForm):
    class Meta:
        model = OpenSpace
        fields = '__all__'


class AvailableFacilityForm(ModelForm):
    class Meta:
        model = AvailableFacility
        fields = '__all__'


class QuestionForm(ModelForm):
    class Meta:
        model = QuestionList
        fields = '__all__'
