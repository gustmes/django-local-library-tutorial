# Generated by Django 3.0.6 on 2020-06-12 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20200606_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='died'),
        ),
    ]