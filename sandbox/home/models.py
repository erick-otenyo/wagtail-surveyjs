from wagtail.models import Page

from wagtailsurveyjs.models import AbstractSurveyJsFormPage


class HomePage(Page):
    pass


class SurveyPage(AbstractSurveyJsFormPage):
    parent_page_types = ['home.HomePage']

    subpage_types = []
    template = "survey_form_page.html"

    content_panels = Page.content_panels
