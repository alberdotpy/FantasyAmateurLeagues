# Generated by Django 4.2.5 on 2023-10-03 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_match_match_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprediction',
            name='sport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.sport'),
            preserve_default=False,
        ),
    ]
