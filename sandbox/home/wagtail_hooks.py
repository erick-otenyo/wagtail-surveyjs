from wagtail.contrib.modeladmin.options import modeladmin_register

from .models import SurveyPage
from wagtailsurveyjs.wagtail_hooks import BaseSurveyModelAdmin


class SurveyModelAdmin(BaseSurveyModelAdmin):
    model = SurveyPage
    menu_label = 'Surveys'
    menu_icon = 'folder-inverse'
    menu_order = 700


modeladmin_register(SurveyModelAdmin)
