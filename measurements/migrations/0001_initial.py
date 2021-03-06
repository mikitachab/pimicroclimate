# Generated by Django 2.2 on 2019-05-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.IntegerField()),
                ('humidity', models.IntegerField()),
                ('light', models.IntegerField()),
                ('is_loud', models.BooleanField()),
                ('is_valid', models.BooleanField()),
                ('datetime', models.DateTimeField()),
            ],
        ),
    ]
