# Generated by Django 4.2 on 2023-05-20 12:02

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
                ("nn", models.CharField(max_length=12)),
                ("name", models.CharField(default="", max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=20)),
                (
                    "identification",
                    models.CharField(
                        default="", max_length=20, primary_key=True, serialize=False
                    ),
                ),
                ("username", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "Passenger",
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
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticket_number", models.CharField(max_length=20)),
                ("status", models.CharField(max_length=20)),
                ("departure_datetime", models.DateTimeField()),
                ("arrival_datetime", models.DateTimeField()),
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
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("parking_number", models.CharField(max_length=20)),
                ("status", models.CharField(max_length=20)),
                ("duration", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.passenger",
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
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("luggage_number", models.CharField(max_length=20)),
                ("weight", models.DecimalField(decimal_places=2, max_digits=3)),
                ("status", models.CharField(max_length=20)),
                ("position", models.CharField(max_length=20)),
                (
                    "passenger",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airport.passenger",
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
        migrations.CreateModel(
            name="Flight",
            fields=[
                (
                    "flight_number",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("departure_datetime", models.DateTimeField()),
                ("arrival_datetime", models.DateTimeField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(max_length=20)),
                (
                    "gate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="airport.gate"
                    ),
                ),
                (
                    "runway",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="airport.runway"
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
                "db_table": "Flight",
            },
        ),
    ]
