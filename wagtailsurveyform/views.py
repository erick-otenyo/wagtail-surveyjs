import json

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView

from wagtailsurveyform.models import SurveyFormPage, SurveySettings, SurveyFormSubmission
from wagtailsurveyform.serializers import SurveyFormPageSerializer, SurveyFormSubmissionSerializer


def survey_creator(request, survey_id):
    survey = get_object_or_404(SurveyFormPage, pk=survey_id)
    survey_settings = SurveySettings.for_request(request=request)

    settings = {
        "has_license": survey_settings.has_license
    }

    context = {
        "survey": survey,
        "settings": json.dumps(settings),

    }
    return render(request, "admin_survey_creator.html", context)


def survey_results(request, survey_id):
    survey = get_object_or_404(SurveyFormPage, pk=survey_id)
    survey_settings = SurveySettings.for_request(request=request)

    settings = {
        "has_license": survey_settings.has_license
    }

    context = {
        "survey": survey,
        "survey_data_url": reverse("survey_data", args=[survey.pk]),
        "settings": json.dumps(settings),
    }

    return render(request, "admin_survey_results.html", context)


class SurveyDetailView(APIView):
    def put(self, request, survey_id):
        saved_survey = get_object_or_404(SurveyFormPage.objects.all(), pk=survey_id)

        serializer = SurveyFormPageSerializer(
            instance=saved_survey, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            survey_saved = serializer.save()

            return Response({
                "success": "Survey '{}' updated successfully".format(survey_saved.name)
            })


class SurveySubmissionAPIView(APIView):
    def post(self, request, survey_id):
        serializer = SurveyFormSubmissionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            "success": "Survey submitted successfully"
        })

    def get(self, request, survey_id):
        submissions = SurveyFormSubmission.objects.filter(page=survey_id)
        survey = SurveyFormPage.objects.get(pk=survey_id)
        survey_data = SurveyFormPageSerializer(survey).data
        submissions_data = SurveyFormSubmissionSerializer(submissions, many=True).data
        response_data = {
            "survey": survey_data,
            "results": submissions_data
        }
        return Response(response_data)
