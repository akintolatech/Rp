# Generated by Django 3.2.8 on 2023-07-17 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0014_alter_customuser_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='subject',
            field=models.CharField(max_length=255),
        ),
    ]