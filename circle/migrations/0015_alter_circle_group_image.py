# Generated by Django 4.0.2 on 2022-04-05 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("circle", "0014_alter_circle_group_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="circle",
            name="group_image",
            field=models.ImageField(
                blank=True,
                default="media/default/circle/1",
                null=True,
                upload_to="media/",
            ),
        ),
    ]