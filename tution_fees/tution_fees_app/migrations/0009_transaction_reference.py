# Generated by Django 3.1 on 2021-01-10 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tution_fees_app', '0008_auto_20210110_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
