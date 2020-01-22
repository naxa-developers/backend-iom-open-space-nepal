from django.forms import ModelForm
from core.models import OpenSpace, AvailableFacility, QuestionList, QuestionsData, SuggestedUseList, SuggestedUseData, \
    ServiceList, ServiceData, ResourceCategory, Slider, CreateOpenSpace

from front.models import Header, OpenSpaceApp, OpenSpaceIde, Contact, OpenSpaceDef


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


class ResourceCategoryForm(ModelForm):
    class Meta:
        model = ResourceCategory
        fields = '__all__'


#front views from
class HeaderForm(ModelForm):
    class Meta:
        model = Header
        fields = '__all__'


class SliderForm(ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'


class CreateOpenSpaceForm(ModelForm):
    class Meta:
        model = CreateOpenSpace
        fields = '__all__'


class OpenSpaceIdeForm(ModelForm):
    class Meta:
        model = OpenSpaceIde
        fields = '__all__'


class OpenSpaceDefForm(ModelForm):
    class Meta:
        model = OpenSpaceDef
        fields = '__all__'


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class OpenSpaceAppForm(ModelForm):
    class Meta:
        model = OpenSpaceApp
        fields = '__all__'


