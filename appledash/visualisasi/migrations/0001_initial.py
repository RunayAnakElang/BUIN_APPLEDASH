# Generated by Django 5.2.1 on 2025-06-13 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PenjualanApple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('iphone_sales', models.FloatField()),
                ('ipad_sales', models.FloatField()),
                ('mac_sales', models.FloatField()),
                ('wearables', models.FloatField()),
                ('services_revenue', models.FloatField()),
            ],
        ),
    ]
