from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.admin.edit_handlers import MultiFieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class Heading(blocks.StructBlock):
    caption = blocks.CharBlock(required=False, max_length=255, template='custom_blocks/headings.html')
    heading = blocks.CharBlock(required=True, classname='full title', max_length=255, template='custom_blocks/headings.html')


class GreenPanel(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=255, classname='full title')
    body = blocks.TextBlock(required=True, classname='full')


streamfield_args = [
    (
        'heading',
        Heading(
            classname="xl",
            template='custom_blocks/headings.html',
            icon='title'
        )
    ),
    (
        'h2',
        Heading(
            classname="l",
            template='custom_blocks/headings.html'
        )
    ),
    (
        'h3',
        Heading(
            classname="m",
            template='custom_blocks/headings.html'
        )
    ),
    (
        'h4',
        blocks.CharBlock(
            classname="full title",
            required=True,
            template='custom_blocks/headings.html'
        )
    ),
    (
        'govuk_ul',
        blocks.ListBlock(
            blocks.RichTextBlock(
                features=['bold', 'italic', 'link']
            ),
            classname="full",
            template='custom_blocks/govuk_ul.html'
        )
    ),
    (
        'blockquote',
        blocks.TextBlock(classname="full", icon='arrow-right')
    ),
    (
        'paragraph',
         blocks.RichTextBlock(
            classname='full',
            features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link']
         )
     ),
    (
        'green_panel',
        GreenPanel(
            classname='green_panel',
            template='custom_blocks/govuk_panel.html',
            icon='form'
        )
    ),
    ('image', ImageChooserBlock()),
]


class BlogIndex(RoutablePageMixin, Page):

    body = StreamField(streamfield_args)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    # @property
    # def blog_page(self):
    #     return self.get_parent().specific
    #
    # def get_context(self, request, *args, **kwargs):
    #     context = super(BlogIndex, self).get_context(request, *args, **kwargs)
    #     context['posts'] = self.blog_page
    #     context['blog_page'] = self
    #
    #     context['menuitems'] = self.get_children().filter(
    #         live=True, show_in_menus=True)
    #
    #     return context


class CustomRichTextField(blocks.RichTextBlock):
    def get_prep_value(self, value):
        # convert a RichText object back to a source-HTML string to go into
        # the JSONish representation


        ref = {
            'a': 'govuk-link govuk-link--no-visited-state'
        }

        result = str()

        from lxml.etree import HTMLParser, fromstring  # , tostring, tostringlist
        from lxml.html import tostring

        parser = HTMLParser()

        tree = fromstring(value.source, parser=parser)
        for node in tree:
            cls = ref.get(node.tag)
            if cls is not None:
                node.attr['class'] = cls

            result += tostring(node).decode()  # .lstrip('<body>').rstrip('</body>')

        # value.source = result # tostring(tree, ).decode()
        return value.source


class BlogPage(RoutablePageMixin, Page):
    body = StreamField(streamfield_args)
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]

    # Parent page / subpage type rules
    parent_page_types = ['pages.BlogIndex']
    subpage_types = []

    @property
    def blog_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.blog_page
        context['blog_page'] = self

        context['menuitems'] = self.get_children().filter(live=True, show_in_menus=True)

        print(context)

        return context


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
