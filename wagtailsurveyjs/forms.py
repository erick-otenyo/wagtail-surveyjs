from django import forms

from wagtailsurveyjs.models import SurveyJsCreatorFileUpload, SurveyJsSubmissionFileUpload


class SurveyJsCreatorFileUploadForm(forms.ModelForm):
    class Meta:
        model = SurveyJsCreatorFileUpload
        fields = "__all__"


class SurveyJsSubmissionUploadForm(forms.ModelForm):
    class Meta:
        model = SurveyJsSubmissionFileUpload
        fields = "__all__"
