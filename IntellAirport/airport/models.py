from django.db import models

# Create your models here.
import random


def generate_random_number():
    return str(random.randint(100000000, 999999999))


class Passenger(models.Model):
    name = models.CharField(max_length=20, unique=True, default="UnKnown")
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True, default="Unknown")
    identification = models.CharField(max_length=20, unique=True, default="Unknown")
    username = models.CharField(max_length=20, unique=True, default="Unknown")
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatar', null=True)

    class Meta:
        db_table = 'Passenger'
        unique_together = ('name', 'identification', 'phone_number', 'username')


class Luggage(models.Model):
    luggage_number = models.CharField(max_length=20, primary_key=True)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, to_field='identification')

    class Meta:
        db_table = 'Luggage'


class Parking(models.Model):
    parking_number = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(max_length=20)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, to_field='identification')
    duration = models.DateTimeField()
    start_time = models.DateTimeField(auto_now_add=True)  # 开始时间，创建时更新
    end_time = models.DateTimeField(auto_now=True)  # 结束时间，最后一次修改表时更新

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
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    airline_name = models.ForeignKey('Airline', on_delete=models.CASCADE, to_field='name')
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
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    flight_number = models.ForeignKey(Flight, on_delete=models.CASCADE, to_field='flight_number')
    airline_name = models.ForeignKey(Airline, on_delete=models.CASCADE, to_field='name')
    ticket_number_random = models.CharField(max_length=20, primary_key=True, default=generate_random_number)
    status = models.CharField(max_length=20)
    departure_datetime = models.DateTimeField()  # TODO:需要设置外键
    arrival_datetime = models.DateTimeField()  # TODO:需要设置外键
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, to_field='terminal_number')
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, to_field='gate_number')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, to_field='identification')

    class Meta:
        db_table = 'Ticket'


class Device(models.Model):
    dev_id = models.CharField(max_length=20)
    dev_name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='devices', null=True)
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'Device'


class Store(models.Model):
    store_id = models.CharField(max_length=20, primary_key=True)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, to_field='id')
    store_name = models.CharField(max_length=20)
    store_image = models.ImageField(upload_to='stores', null=True)

    class Meta:
        db_table = 'Store'
