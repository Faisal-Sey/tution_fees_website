# Generated by Django 3.1 on 2021-01-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tution_fees_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=10)),
                ('Balance', models.IntegerField()),
                ('Slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
    ]
