# Generated by Django 4.2.9 on 2025-02-25 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_first_purchase',
            field=models.BooleanField(default=False),
        ),
    ]
