# Generated by Django 2.1 on 2018-09-27 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='device',
            field=models.CharField(default='powerstrip', max_length=100),
        ),
    ]
