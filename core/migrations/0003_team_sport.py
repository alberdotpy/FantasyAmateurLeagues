# Generated by Django 4.2.5 on 2023-09-30 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_league_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='sport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.sport'),
            preserve_default=False,
        ),
    ]
