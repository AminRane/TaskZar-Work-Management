# Generated by Django 3.2.6 on 2021-09-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('Done', 'Done'), ('In Progress', 'In Progress'), ('To Do', 'To Do')], default='Pending', max_length=200, null=True),
        ),
    ]
