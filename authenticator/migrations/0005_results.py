# Generated by Django 3.2.8 on 2023-07-16 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0004_alter_customuser_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=255)),
                ('cat1', models.IntegerField()),
                ('cat2', models.IntegerField()),
                ('exam', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
    ]