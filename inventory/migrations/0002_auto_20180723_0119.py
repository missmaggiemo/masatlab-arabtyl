# Generated by Django 2.0.7 on 2018-07-23 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='activation_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='deactivation_date',
            field=models.DateTimeField(null=True),
        ),
    ]