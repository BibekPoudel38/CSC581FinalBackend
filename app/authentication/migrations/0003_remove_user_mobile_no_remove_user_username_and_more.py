# Generated by Django 4.2.2 on 2025-04-25 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_user_date_joined_remove_user_is_mentor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile_no',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
