# Generated by Django 4.0.2 on 2022-04-13 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="home_alert_case",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alert",
            name="home_alert_death",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alert",
            name="location_alert_case",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alert",
            name="location_alert_death",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alert",
            name="location_data_case",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="alert",
            name="location_data_death",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="alert",
            name="people_alert",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alert", name="people_data", field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="alert",
            name="work_alert_case",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alert",
            name="work_alert_death",
            field=models.BooleanField(default=False),
        ),
    ]
