from wagtail.core.rich_text import LinkHandler
from wagtail.core.models import Page
from wagtail.core import hooks, blocks

from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail.admin.rich_text.editors.draftail import features as draftail_features

from django.utils.html import escape


class ExternalLinkHandler(LinkHandler):
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return f'<a href="{escape(href)}" class="govuk-link" rel="noopener nofollower" target="_blank">'


@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(ExternalLinkHandler)


class PageLinkHandler(LinkHandler):
    identifier = 'page'

    @staticmethod
    def get_model():
        return Page

    @classmethod
    def get_instance(cls, attrs):
        instance = super().get_instance(attrs)
        return getattr(instance, 'specific')

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            page = cls.get_instance(attrs)
            specific = getattr(page, 'specific')
            return '<a href="%s" class="govuk-link govuk-link--no-visited-state">' % escape(specific.url)
        except Page.DoesNotExist:
            return '<a  class="govuk-link govuk-link--no-visited-state">'


@hooks.register('register_rich_text_features')
def register_page_link(features):
    features.register_link_type(PageLinkHandler)


class ColumnBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock(
        features=['bold', 'italic', 'link']
    )

    # class Meta:
    #     template = 'blog/blocks/column.html'


# @hooks.register('register_rich_text_features')
# def register_govuk_li_feature(features):
#     """
#     Registering the `help-text` feature, which uses the `help-text` Draft.js block type,
#     and is stored as HTML with a `<div class="help-text">` tag.
#     """
#     feature_name = 'govuk_ul'
#     type_ = 'GOVUK_UL'
#
#     control = {
#         'type': type_,
#         'label': 'UnL',
#         'description': 'Unordered List',
#         # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
#         'element': 'li',
#     }
#
#     features.register_editor_plugin(
#         'draftail',
#         feature_name,
#         draftail_features.BlockFeature(control)
#     )
#
#     features.register_converter_rule('contentstate', feature_name, {
#         'from_database_format': {'li.govuk_li': BlockElementHandler(type_)},
#         'to_database_format': {
#             'block_map': {
#                 type_: {
#                     'element': 'li',
#                     'props': {'class': 'li'}
#                 }
#             }
#         },
#     })
