# Generated by Django 4.2 on 2023-05-25 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="device",
            name="id",
        ),
        migrations.AlterField(
            model_name="device",
            name="dev_id",
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]