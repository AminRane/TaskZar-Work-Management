# Generated by Django 3.2.8 on 2021-10-30 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0025_auto_20211030_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='profile_picture',
            field=models.ImageField(default='./static/images/user-profile-default.png', upload_to='profile_pictures'),
        ),
    ]
