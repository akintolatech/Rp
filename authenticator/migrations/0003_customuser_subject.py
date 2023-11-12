# Generated by Django 3.2.8 on 2023-07-16 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0002_remove_customuser_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='subject',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='authenticator.subject'),
            preserve_default=False,
        ),
    ]
