# Generated by Django 3.2.8 on 2021-10-16 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0014_auto_20211015_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='p_manager',
            new_name='project_manager',
        ),
    ]