from django.urls import path

from .views import SurveyDetailView, SurveySubmissionAPIView

urlpatterns = [
    path('api/surveys-update/<int:survey_id>/', SurveyDetailView.as_view(), name="update_survey_json"),
    path('api/survey-data/<int:survey_id>/', SurveySubmissionAPIView.as_view(), name="survey_data"),
]
