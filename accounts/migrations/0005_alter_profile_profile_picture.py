# Generated by Django 4.1.7 on 2023-05-02 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_about_me_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/Default_profile_picture.svg', upload_to='profile_pictures/'),
        ),
    ]