# Generated by Django 2.0.13 on 2019-10-07 11:18

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20191006_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogindex',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(classname='full', features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link'])), ('image', wagtail.images.blocks.ImageChooserBlock())]),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(max_length=255, required=False, template='custom_blocks/headings.html')), ('heading', wagtail.core.blocks.CharBlock(classname='full title', max_length=255, required=True, template='custom_blocks/headings.html'))], classname='xl', template='custom_blocks/headings.html')), ('h2', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(max_length=255, required=False, template='custom_blocks/headings.html')), ('heading', wagtail.core.blocks.CharBlock(classname='full title', max_length=255, required=True, template='custom_blocks/headings.html'))], classname='l', template='custom_blocks/headings.html')), ('h3', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(max_length=255, required=False, template='custom_blocks/headings.html')), ('heading', wagtail.core.blocks.CharBlock(classname='full title', max_length=255, required=True, template='custom_blocks/headings.html'))], classname='m', template='custom_blocks/headings.html')), ('h4', wagtail.core.blocks.CharBlock(classname='full title', required=True, template='custom_blocks/headings.html')), ('govuk_ul', wagtail.core.blocks.ListBlock(wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link']), classname='full', template='custom_blocks/govuk_ul.html')), ('blockquote', wagtail.core.blocks.CharBlock(classname='full')), ('paragraph', wagtail.core.blocks.RichTextBlock(classname='full', features=['bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link'])), ('green_panel', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(classname='full title', max_length=255, required=False)), ('body', wagtail.core.blocks.TextBlock(classname='full', required=True))], classname='green_panel', template='custom_blocks/govuk_panel.html')), ('image', wagtail.images.blocks.ImageChooserBlock())]),
        ),
    ]
