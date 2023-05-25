import json

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.models import Page

from .models import SurveySettings, SurveyFormSubmission
from .serializers import SurveyFormPageSerializer, SurveyFormSubmissionSerializer


def survey_creator(request, survey_id):
    page = get_object_or_404(Page, pk=survey_id)

    survey = page.specific

    survey_settings = SurveySettings.for_request(request=request)

    settings = {
        "has_license": survey_settings.has_license
    }

    context = {
        "survey": survey,
        "settings": json.dumps(settings),
    }

    parent_page = survey.get_parent()
    if parent_page:
        context.update({"explore_url": reverse("wagtailadmin_explore", args=[parent_page.id])})

    return render(request, "wagtailsurveyjs/admin_survey_creator.html", context)


def survey_results(request, survey_id):
    page = get_object_or_404(Page, pk=survey_id)

    survey = page.specific

    survey_settings = SurveySettings.for_request(request=request)

    settings = {
        "has_license": survey_settings.has_license
    }

    context = {
        "survey": survey,
        "survey_data_url": reverse("survey_data", args=[survey.pk]),
        "settings": json.dumps(settings),
    }

    return render(request, "wagtailsurveyjs/admin_survey_results.html", context)


class SurveyDetailView(APIView):
    def put(self, request, survey_id):
        page = get_object_or_404(Page.objects.all(), pk=survey_id)
        saved_survey = page.specific

        # get model class
        model = saved_survey._meta.model
        SurveyFormPageSerializer.Meta.model = model

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
        page = Page.objects.get(pk=survey_id)
        survey = page.specific
        # get model class
        model = survey._meta.model
        SurveyFormPageSerializer.Meta.model = model

        survey_data = SurveyFormPageSerializer(survey).data
        submissions_data = SurveyFormSubmissionSerializer(submissions, many=True).data
        response_data = {
            "survey": survey_data,
            "results": submissions_data
        }
        return Response(response_data)
