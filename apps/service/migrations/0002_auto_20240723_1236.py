# Generated by Django 2.2.7 on 2024-07-23 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_tax',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
    ]
