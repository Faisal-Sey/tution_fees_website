# Generated by Django 3.1 on 2021-01-10 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tution_fees_app', '0009_transaction_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(),
        ),
    ]
