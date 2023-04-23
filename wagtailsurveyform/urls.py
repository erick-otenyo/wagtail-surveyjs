from django.urls import path

from wagtailsurveyform.views import SurveyDetailView, SurveySubmissionAPIView

urlpatterns = [
    path('api/surveys/<int:survey_id>', SurveyDetailView.as_view(), name="update_survey_json"),
    path('api/surveys/data/<int:survey_id>', SurveySubmissionAPIView.as_view(), name="survey_data"),
]
