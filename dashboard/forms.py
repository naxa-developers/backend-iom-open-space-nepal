from django.forms import ModelForm
from core.models import OpenSpace, AvailableFacility, QuestionList, QuestionsData, SuggestedUseList


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


class QuestionDataForm(ModelForm):
    class Meta:
        model = QuestionsData
        fields = '__all__'


class SuggestedForm(ModelForm):
    class Meta:
        model = SuggestedUseList
        fields = '__all__'
