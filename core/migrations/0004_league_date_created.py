# Generated by Django 4.2.5 on 2023-10-01 16:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_team_sport'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
