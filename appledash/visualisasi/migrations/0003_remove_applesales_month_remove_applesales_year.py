# Generated by Django 5.2.1 on 2025-06-14 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualisasi', '0002_rename_penjualanapple_applesales'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applesales',
            name='month',
        ),
        migrations.RemoveField(
            model_name='applesales',
            name='year',
        ),
    ]
