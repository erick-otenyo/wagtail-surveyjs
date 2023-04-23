from django.urls import path
from django.utils.safestring import mark_safe
from wagtail import hooks
from wagtail.admin.action_menu import ActionMenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from wagtailsurveyform.models import SurveyFormPage
from wagtailsurveyform.views import survey_creator, survey_results


@hooks.register('register_admin_urls')
def urlconf_wagtailsurveyform():
    return [
        path('survey-creator/<int:survey_id>/', survey_creator, name='survey_creator'),
        path('survey-results/<int:survey_id>/', survey_results, name='survey_results'),
    ]


class SurveyModelAdmin(ModelAdmin):
    model = SurveyFormPage

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['survey_creator', "view_submissions"]
        self.survey_creator.__func__.short_description = f'Survey Creator'
        self.view_submissions.__func__.short_description = f'View Submissions'

    def survey_creator(self, obj):
        button_html = f"""
        <a href="{obj.get_survey_creator_url()}" class="button button-small bicolor button--icon">
            <span class="icon-wrapper">
                <svg class="icon icon-clipboard-list icon" aria-hidden="true">
                    <use href="#icon-clipboard-list"></use>
                </svg>
            </span>
        Survey Creator
        </a>
        """
        return mark_safe(button_html)

    def view_submissions(self, obj):
        button_html = f"""
        <a href="{obj.get_survey_results_url()}" class="button button-small button--icon button-secondary">
            <span class="icon-wrapper">
                <svg class="icon icon-plus icon" aria-hidden="true">
                    <use href="#icon-view"></use>
                </svg>
            </span>
        View Submissions
        </a>
        """
        return mark_safe(button_html)


class SurveyAdminGroup(ModelAdminGroup):
    menu_label = 'Surveys'
    menu_icon = 'folder-inverse'
    menu_order = 700
    items = (SurveyModelAdmin,)

    def get_submenu_items(self):
        menu_items = []
        item_order = 1
        for model_admin in self.modeladmin_instances:
            menu_items.append(model_admin.get_menu_item(order=item_order))
            item_order += 1

        # survey_creator = MenuItem(label="Survey Creator", url="#", icon_name="cog")
        # menu_items.append(survey_creator)

        return menu_items


modeladmin_register(SurveyAdminGroup)


class SurveyCreatorMenuItem(ActionMenuItem):
    name = 'action-survey-creator'
    label = "Survey Creator"

    def is_shown(self, context):
        page = context.get("page")
        if isinstance(page, SurveyFormPage):
            return True
        return False

    def get_url(self, context):
        page = context.get("page")
        return page.get_survey_creator_url()


@hooks.register('register_page_action_menu_item')
def register_guacamole_menu_item():
    return SurveyCreatorMenuItem(order=10)
