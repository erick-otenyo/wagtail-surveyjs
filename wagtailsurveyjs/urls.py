from django.urls import path

from .views import SurveyDetailView, SurveySubmissionAPIView, SurveySubmissionFileUploadAPIView

urlpatterns = [
    path('api/surveys-update/<int:survey_id>/', SurveyDetailView.as_view(), name="update_survey_json"),
    path('api/survey-data/json/<int:survey_id>/', SurveySubmissionAPIView.as_view(), name="survey_data"),
    path('api/survey-data/uploads/<int:survey_id>/', SurveySubmissionFileUploadAPIView.as_view(),
         name="survey_uploads"),
]
