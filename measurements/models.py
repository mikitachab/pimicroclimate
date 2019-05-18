from django.db import models


class Measurement(models.Model):
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    light = models.IntegerField()
    is_loud = models.BooleanField()
    is_valid = models.BooleanField()
    datetime = models.DateTimeField()


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
