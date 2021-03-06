from django import forms
from django.forms import ModelForm
from core.models import OpenSpace, AvailableFacility, QuestionList, QuestionsData, SuggestedUseList, SuggestedUseData, \
    ServiceList, ServiceData, ResourceCategory, Slider, CreateOpenSpace, Gallery, Resource, ResourceDocumentType, \
    AvailableType, CreateOpenSpacePoints, MainOpenSpace, MunicipalityQuestionsData, CommunitySpace, MainCommunitySpace

from front.models import Header, OpenSpaceApp, OpenSpaceIde, Contact, OpenSpaceDef, WhyMapOpenSpace, WhyMapOpenIcon, \
    AboutHeader, OpenSpaceCriteria, CriteriaType, CriteriaDescription
from dashboard.models import AgencyMessage


class AgencyMessageForm(ModelForm):
    class Meta:
        model = AgencyMessage
        fields = '__all__'


class OpenSpaceForm(ModelForm):

    longitude = forms.CharField(required=False)
    latitude = forms.CharField(required=False)
    polygon_shp = forms.FileField(required=False)

    class Meta:
        model = OpenSpace
        exclude = ('polygons', )


class CommunitySpaceForm(ModelForm):

    longitude = forms.CharField(required=False)
    latitude = forms.CharField(required=False)
    polygon_shp = forms.FileField(required=False)

    class Meta:
        model = CommunitySpace
        exclude = ('polygons', )


class AvailableFacilityCreateUpdateForm(ModelForm):

    longitude = forms.CharField()
    latitude = forms.CharField()

    class Meta:
        model = AvailableFacility
        fields = ('name', 'ward_no', 'phone_number', 'comments', 'longitude', 'latitude', 'op_type')


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


# front views from
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


class OpenSpaceIdeForm(ModelForm):
    class Meta:
        model = OpenSpaceIde
        fields = '__all__'


class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceDocumentTypeForm(ModelForm):
    class Meta:
        model = ResourceDocumentType
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


class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'


class AvailableTypeForm(ModelForm):
    class Meta:
        model = AvailableType
        fields = '__all__'


class WhyMapOpenSpaceForm(ModelForm):
    class Meta:
        model = WhyMapOpenSpace
        fields = '__all__'


class WhyMapOpenSpaceIconForm(ModelForm):
    class Meta:
        model = WhyMapOpenIcon
        fields = '__all__'


class AboutHeaderForm(ModelForm):
    class Meta:
        model = AboutHeader
        fields = '__all__'


class OpenSpaceCriteriaForm(ModelForm):
    class Meta:
        model = OpenSpaceCriteria
        fields = '__all__'


class CriteriaTypeForm(ModelForm):
    class Meta:
        model = CriteriaType
        fields = '__all__'


class CriteriaDescriptionForm(ModelForm):
    class Meta:
        model = CriteriaDescription
        fields = '__all__'


class CreateOpenSpacePointsForm(ModelForm):
    class Meta:
        model = CreateOpenSpacePoints
        fields = '__all__'


CHARACTER_ENCODINGS = [("ascii", "ASCII"),
                       ("latin1", "Latin-1"),
                       ("utf8", "UTF-8")]


class ImportShapefileForm(forms.Form):
    """ This form defines the parameters used to import a shapefile.
    """
    import_file = forms.FileField(label="Select a Zipped Shapefile")
    character_encoding = forms.ChoiceField(choices=CHARACTER_ENCODINGS,
                                           initial="utf8")


class UploadNewOpenSpaceForm(forms.Form):
    open_space = forms.FileField()
    eia_table = forms.FileField()
    nearby_amenities = forms.FileField()


class MunicipalityQuestionsDataForm(forms.ModelForm):
    eia = forms.FileField()

    class Meta:
        model = MunicipalityQuestionsData
        exclude = ()


class MainOpenSpaceForm(forms.ModelForm):
    open_space = forms.FileField()
    open_space_shp = forms.FileField()

    class Meta:
        model = MainOpenSpace
        fields = ('project_title', 'description', 'municipality', 'open_space', 'open_space_shp')


class MainCommunitySpaceForm(forms.ModelForm):
    community_space = forms.FileField()
    community_space_shp = forms.FileField()

    class Meta:
        model = MainCommunitySpace
        fields = ('project_title', 'description', 'municipality', 'community_space', 'community_space_shp')
