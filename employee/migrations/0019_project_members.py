# Generated by Django 3.2.8 on 2021-10-19 07:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0018_project_teammember'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(through='employee.TeamMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
