# Generated by Django 4.0.2 on 2022-04-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0003_alertnotification"),
    ]

    operations = [
        migrations.AddField(
            model_name="alertnotification",
            name="updated",
            field=models.DateTimeField(default=None),
        ),
    ]
