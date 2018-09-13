# Generated by Django 2.1 on 2018-09-10 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DevicesReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_firstName', models.CharField(max_length=100)),
                ('user_secondName', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('device', models.CharField(max_length=100)),
                ('purpose', models.TextField()),
                ('comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_firstName', models.CharField(max_length=100)),
                ('user_secondName', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('reservation_labor', models.BooleanField()),
                ('reservation_studio', models.BooleanField()),
                ('reservation_workshop', models.BooleanField()),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('purpose', models.TextField()),
                ('comments', models.TextField(blank=True)),
            ],
        ),
    ]
