# Generated by Django 3.2.6 on 2021-09-05 00:57

from django.db import migrations, models
import django.db.models.deletion
import home.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.core.fields.StreamField([('generic_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('fields', wagtail.core.blocks.StreamBlock([('text', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock())])), ('container', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock())])))])), ('block_id', home.blocks.IDBlock(label='--', required=False))]))), ('stream', wagtail.core.blocks.StreamBlock([('form', wagtail.core.blocks.StructBlock([('fields', wagtail.core.blocks.StreamBlock([('text', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock())])), ('container', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock())])))])), ('block_id', home.blocks.IDBlock(label='--', required=False))]))])), ('form', wagtail.core.blocks.StructBlock([('fields', wagtail.core.blocks.StreamBlock([('text', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock())])), ('container', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock())])))])), ('block_id', home.blocks.IDBlock(label='--', required=False))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
