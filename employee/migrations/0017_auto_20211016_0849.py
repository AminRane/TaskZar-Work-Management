# Generated by Django 3.2.8 on 2021-10-16 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0016_project_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='project',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
