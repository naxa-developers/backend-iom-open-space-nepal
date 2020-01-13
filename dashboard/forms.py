from django.forms import ModelForm
from core.models import OpenSpace, AvailableFacility, QuestionList, QuestionsData, SuggestedUseList, SuggestedUseData, \
    ServiceList, ServiceData


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


class SuggestedDataForm(ModelForm):
    class Meta:
        model = SuggestedUseData
        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = ServiceList
        fields = '__all__'


class ServiceDataForm(ModelForm):
    class Meta:
        model = ServiceData
        fields = '__all__'
