# Generated by Django 4.2.4 on 2023-09-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0016_alter_reservation_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_number',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]
