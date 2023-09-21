# Generated by Django 3.2.8 on 2021-10-16 03:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0015_rename_p_manager_project_project_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='member',
            field=models.ManyToManyField(blank=True, null=True, related_name='member', to=settings.AUTH_USER_MODEL),
        ),
    ]
