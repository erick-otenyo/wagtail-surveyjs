from wagtail_modeladmin.options import modeladmin_register, ModelAdminGroup

from wagtailsurveyjs.wagtail_hooks import BaseSurveyModelAdmin
from .models import SurveyPage


class SurveyModelAdmin(BaseSurveyModelAdmin):
    model = SurveyPage
    menu_label = 'Surveys'
    menu_icon = 'folder-inverse'
    menu_order = 700


modeladmin_register(SurveyModelAdmin)
