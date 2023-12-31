# Generated by Django 4.2.4 on 2023-09-01 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0010_alter_rooms_room_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_first_name', models.CharField(max_length=100)),
                ('client_last_name', models.CharField(max_length=100)),
                ('client_dob', models.DateField()),
                ('client_phno', models.IntegerField()),
                ('client_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
