# Generated by Django 4.2 on 2023-05-20 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0002_remove_passenger_nn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passenger",
            name="email",
            field=models.EmailField(max_length=255),
        ),
    ]
