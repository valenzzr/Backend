# Generated by Django 4.2 on 2023-05-22 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0002_remove_ticket_id_alter_ticket_ticket_number"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="ticket",
            table="Ticket",
        ),
    ]
