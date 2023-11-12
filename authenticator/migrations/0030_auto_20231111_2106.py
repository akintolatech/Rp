# Generated by Django 3.2.8 on 2023-11-11 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0029_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='form',
            field=models.CharField(default='REM 6', max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.CharField(default='2023', max_length=255),
        ),
    ]