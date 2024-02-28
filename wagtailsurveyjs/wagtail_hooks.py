from django.urls import path
from django.utils.safestring import mark_safe
from wagtail import hooks
from wagtail.admin import widgets as wagtail_admin_widgets
from wagtail.admin.action_menu import ActionMenuItem
from wagtail_modeladmin.options import ModelAdmin

from .models import AbstractSurveyJsFormPage
from .views import survey_creator, survey_results


@hooks.register('register_admin_urls')
def urlconf_wagtailsurveyform():
    return [
        path('survey-creator/<int:survey_id>/', survey_creator, name='survey_creator'),
        path('survey-results/<int:survey_id>/', survey_results, name='survey_results'),
    ]


class BaseSurveyModelAdmin(ModelAdmin):
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


class SurveyCreatorMenuItem(ActionMenuItem):
    name = 'action-survey-creator'
    label = "Survey Creator"

    def is_shown(self, context):
        page = context.get("page")
        if isinstance(page, AbstractSurveyJsFormPage):
            return True
        return False

    def get_url(self, context):
        page = context.get("page")
        return page.get_survey_creator_url()


@hooks.register('register_page_action_menu_item')
def register_survejs_creator_menu_item(*args):
    return SurveyCreatorMenuItem(order=10)


@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, next_url=None):
    if isinstance(page, AbstractSurveyJsFormPage):
        creator_url = page.get_survey_creator_url()

        yield wagtail_admin_widgets.PageListingButton(
            "Survey Creator",
            creator_url,
            priority=50
        )

        if page.live:
            results_url = page.get_survey_results_url()
            yield wagtail_admin_widgets.PageListingButton(
                "Survey Results",
                results_url,
                priority=60
            )
