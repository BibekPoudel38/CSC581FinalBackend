# Generated by Django 4.2.2 on 2025-04-26 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobpost_apply_link_jobpost_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='company_name',
            field=models.CharField(default='google', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobpost',
            name='location',
            field=models.CharField(default='Los Angeles', max_length=255),
            preserve_default=False,
        ),
    ]
