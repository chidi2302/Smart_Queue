# Generated by Django 5.1.1 on 2024-09-26 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queue_app', '0006_booking_user_email_alter_booking_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]
