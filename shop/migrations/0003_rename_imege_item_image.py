# Generated by Django 4.2.5 on 2024-10-05 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_item_imege'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='imege',
            new_name='image',
        ),
    ]
