# Generated by Django 5.2.1 on 2025-07-08 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0005_video_assignment_link_video_pdf_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='playback_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
