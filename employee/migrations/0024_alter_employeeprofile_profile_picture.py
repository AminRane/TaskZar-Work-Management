# Generated by Django 3.2.8 on 2021-10-29 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0023_alter_employeeprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]