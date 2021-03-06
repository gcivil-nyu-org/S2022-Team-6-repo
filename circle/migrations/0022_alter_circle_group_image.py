# Generated by Django 4.0.2 on 2022-04-05 22:46

import circle.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("circle", "0021_alter_circle_group_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="circle",
            name="group_image",
            field=models.ImageField(
                blank=True,
                default=circle.models.random_img,
                null=True,
                upload_to="media/circle/",
            ),
        ),
    ]
