# Generated by Django 4.0.2 on 2022-04-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("circle", "0023_alter_circle_group_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="circle",
            name="display_code",
            field=models.CharField(max_length=8, null=True),
        ),
    ]