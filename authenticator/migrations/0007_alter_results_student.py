# Generated by Django 3.2.8 on 2023-07-16 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0006_auto_20230716_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='student',
            field=models.CharField(max_length=255),
        ),
    ]
