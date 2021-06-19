# Generated by Django 3.1 on 2021-01-08 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tution_fees_app', '0003_auto_20210108_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='details',
            options={'verbose_name_plural': 'Details'},
        ),
        migrations.AddField(
            model_name='details',
            name='items',
            field=models.ManyToManyField(to='tution_fees_app.SignupModel'),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tution_fees_app.details')),
            ],
        ),
    ]