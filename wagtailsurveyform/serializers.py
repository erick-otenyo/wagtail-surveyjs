import json

from rest_framework import serializers

from wagtailsurveyform.models import SurveyFormPage, SurveyFormSubmission


class SurveyFormPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFormPage
        fields = ['json']

    def to_representation(self, instance):
        data = super(SurveyFormPageSerializer, self).to_representation(instance)
        if data.get('json'):
            data["json"] = json.loads(data["json"])
        else:
            data["json"] = {}
        return data


class SurveyFormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFormSubmission
        fields = '__all__'
