# Generated by Django 4.2 on 2023-06-07 21:57

import airport.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Airline",
            fields=[
                (
                    "name",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("contact_number", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "Airline",
            },
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "dev_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("dev_name", models.CharField(max_length=20)),
                ("image", models.ImageField(null=True, upload_to="devices")),
                ("status", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "Device",
            },
        ),
        migrations.CreateModel(
            name="Flight",
            fields=[
                ("origin", models.CharField(max_length=20)),
                ("destination", models.CharField(max_length=20)),
                (
                    "flight_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("departure_datetime", models.DateTimeField()),
                ("arrival_datetime", models.DateTimeField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(max_length=20)),
                (
                    "airline_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.airline",
                    ),
                ),
            ],
            options={
                "db_table": "Flight",
            },
        ),
        migrations.CreateModel(
            name="Gate",
            fields=[
                (
                    "gate_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
            ],
            options={
                "db_table": "Gate",
            },
        ),
        migrations.CreateModel(
            name="Manager",
            fields=[
                ("name", models.CharField(max_length=20)),
                (
                    "manager_id",
                    models.CharField(
                        default="", max_length=20, primary_key=True, serialize=False
                    ),
                ),
                ("username", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "Manager",
            },
        ),
        migrations.CreateModel(
            name="Passenger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(default="UnKnown", max_length=20, unique=True),
                ),
                ("email", models.EmailField(max_length=255)),
                (
                    "phone_number",
                    models.CharField(default="Unknown", max_length=20, unique=True),
                ),
                (
                    "identification",
                    models.CharField(default="Unknown", max_length=20, unique=True),
                ),
                (
                    "username",
                    models.CharField(default="Unknown", max_length=20, unique=True),
                ),
                ("password", models.CharField(max_length=255)),
                ("avatar", models.ImageField(null=True, upload_to="avatar")),
                ("message", models.CharField(default="None", max_length=255)),
            ],
            options={
                "db_table": "Passenger",
                "unique_together": {
                    ("name", "identification", "phone_number", "username")
                },
            },
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("contact_number", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "Shop",
            },
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("name", models.CharField(max_length=20)),
                (
                    "staff_id",
                    models.CharField(
                        default="", max_length=20, primary_key=True, serialize=False
                    ),
                ),
                ("phone_number", models.CharField(max_length=20)),
                ("username", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "Staff",
            },
        ),
        migrations.CreateModel(
            name="Terminal",
            fields=[
                (
                    "terminal_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
            ],
            options={
                "db_table": "Terminal",
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                ("origin", models.CharField(max_length=20)),
                ("destination", models.CharField(max_length=20)),
                (
                    "ticket_number_random",
                    models.CharField(
                        default=airport.models.generate_random_number,
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("status", models.CharField(max_length=20)),
                ("departure_datetime", models.DateTimeField()),
                ("arrival_datetime", models.DateTimeField()),
                (
                    "airline_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.airline",
                    ),
                ),
                (
                    "flight_number",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="airport.flight"
                    ),
                ),
                (
                    "gate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="airport.gate"
                    ),
                ),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.passenger",
                        to_field="identification",
                    ),
                ),
                (
                    "terminal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.terminal",
                    ),
                ),
            ],
            options={
                "db_table": "Ticket",
            },
        ),
        migrations.CreateModel(
            name="Runway",
            fields=[
                (
                    "runway_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("status", models.CharField(max_length=20)),
                (
                    "gate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="airport.gate"
                    ),
                ),
            ],
            options={
                "db_table": "Runway",
            },
        ),
        migrations.CreateModel(
            name="Parking",
            fields=[
                (
                    "parking_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("status", models.CharField(max_length=20)),
                ("duration", models.DateTimeField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(auto_now=True)),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.passenger",
                        to_field="identification",
                    ),
                ),
            ],
            options={
                "db_table": "Parking",
            },
        ),
        migrations.CreateModel(
            name="Luggage",
            fields=[
                ("luggage_number", models.AutoField(primary_key=True, serialize=False)),
                ("weight", models.DecimalField(decimal_places=2, max_digits=3)),
                ("status", models.CharField(max_length=20)),
                ("position", models.CharField(max_length=20)),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.passenger",
                        to_field="identification",
                    ),
                ),
            ],
            options={
                "db_table": "Luggage",
            },
        ),
        migrations.AddField(
            model_name="gate",
            name="terminal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="airport.terminal"
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="gate",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="airport.gate"
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="runway",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="airport.runway"
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="terminal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="airport.terminal"
            ),
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("store_id", models.CharField(max_length=20)),
                ("store_name", models.CharField(max_length=20)),
                ("store_image", models.ImageField(null=True, upload_to="stores")),
                (
                    "shop_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="airport.shop"
                    ),
                ),
            ],
            options={
                "db_table": "Store",
                "unique_together": {("store_id", "shop_id", "store_name")},
            },
        ),
    ]
