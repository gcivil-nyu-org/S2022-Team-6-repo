# Generated by Django 4.0.2 on 2022-03-29 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("selftracking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="selftrack",
            name="streak",
            field=models.IntegerField(default=0),
        ),
    ]
