from django.db import models


# Create your models here.


class Passenger(models.Model):
    name = models.CharField(max_length=20, default="")
    email = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    identification = models.CharField(max_length=20, primary_key=True, default="")
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'Passenger'


class Luggage(models.Model):
    luggage_number = models.CharField(max_length=20)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, to_field='identification')

    class Meta:
        db_table = 'Luggage'


class Parking(models.Model):
    parking_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, to_field='identification')
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Parking'


class Shop(models.Model):
    name = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'Shop'


class Airline(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    contact_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'Airline'


class Manager(models.Model):
    name = models.CharField(max_length=20)
    manager_id = models.CharField(max_length=20, primary_key=True, default='')
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'Manager'


class Staff(models.Model):
    name = models.CharField(max_length=20)
    staff_id = models.CharField(max_length=20, primary_key=True, default='')
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'Staff'


class Flight(models.Model):
    flight_number = models.CharField(max_length=20, primary_key=True)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    terminal = models.ForeignKey(
        'Terminal',
        on_delete=models.CASCADE,
        to_field='terminal_number',
    )
    gate = models.ForeignKey(
        'Gate',
        on_delete=models.CASCADE,
        to_field='gate_number',
    )
    runway = models.ForeignKey(
        'Runway',
        on_delete=models.CASCADE,
        to_field='runway_number',
    )

    class Meta:
        db_table = 'Flight'


class Terminal(models.Model):
    terminal_number = models.CharField(max_length=20, primary_key=True)

    class Meta:
        db_table = 'Terminal'


class Gate(models.Model):
    gate_number = models.CharField(max_length=20, primary_key=True)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, to_field='terminal_number')

    class Meta:
        db_table = 'Gate'


class Runway(models.Model):
    runway_number = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(max_length=20)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, to_field='gate_number')

    class Meta:
        db_table = 'Runway'


class Ticket(models.Model):
    ticket_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, to_field='terminal_number')
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, to_field='gate_number')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, to_field='identification')
