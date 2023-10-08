# Generated by Django 4.2.4 on 2023-09-01 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0011_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_childrens', models.IntegerField()),
                ('no_of_adults', models.IntegerField()),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_reservation', to='hotel.client')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='hotel.rooms')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=150)),
                ('apt', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='hotel.client')),
            ],
        ),
    ]
