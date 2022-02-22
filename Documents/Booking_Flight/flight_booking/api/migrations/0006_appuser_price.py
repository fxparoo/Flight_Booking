# Generated by Django 4.0.2 on 2022-02-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_appuser_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]