# Generated by Django 3.2.8 on 2023-08-13 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0024_auto_20230810_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='qr_code',
            field=models.ImageField(default=True, upload_to='photo/qr/'),
            preserve_default=False,
        ),
    ]
