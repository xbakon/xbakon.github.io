# Generated by Django 4.2.4 on 2023-09-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0017_reservation_reservation_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_number',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
