# Generated by Django 3.2.8 on 2023-08-17 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0028_auto_20230814_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
