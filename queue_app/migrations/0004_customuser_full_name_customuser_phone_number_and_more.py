# Generated by Django 5.1.1 on 2024-09-25 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queue_app', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='', upload_to='profile_pictures/'),
        ),
    ]
