# Generated by Django 3.2.6 on 2021-09-04 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='asignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]