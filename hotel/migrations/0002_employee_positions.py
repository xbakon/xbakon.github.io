# Generated by Django 4.2.4 on 2023-08-26 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('Front Desk', 'Front Desk'), ('Maintainence', 'Maintainence'), ('Housekeeping', 'Housekeeping')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
