from django.db import models


class Measurement(models.Model):
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    light = models.IntegerField()
    is_loud = models.BooleanField()
    is_valid = models.BooleanField()
    datetime = models.DateTimeField()
    device_id = models.ForeignKey('Device', on_delete=models.CASCADE, default=1)


class Device(models.Model):
    name = models.CharField(max_length=30)

# measurements = Table(
#     'measurements', meta,
#     Column('id', Integer, primary_key=True),
#     Column('datetime', DateTime),
#     Column('temperature', Integer),
#     Column('humidity', Integer),
#     Column('light', Integer),
#     Column('is_loud', Boolean),
#     Column('is_valid', Boolean)
# )
