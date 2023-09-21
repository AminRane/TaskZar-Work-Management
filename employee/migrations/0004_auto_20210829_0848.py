# Generated by Django 3.2.6 on 2021-08-29 03:18

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('employee', '0003_auto_20210827_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartOf',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('group', models.CharField(choices=[('Admin', 'Admin'), ('Project Manager', 'Project Manager'), ('Employee', 'Employee')], max_length=20)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.partof'),
        ),
    ]