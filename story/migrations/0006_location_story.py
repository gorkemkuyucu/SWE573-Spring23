# Generated by Django 4.1.7 on 2023-05-01 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0005_rename_mystory_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='story',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='story.story'),
        ),
    ]
