# Generated by Django 3.2.8 on 2023-07-20 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0020_auto_20230720_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='authenticator.student'),
        ),
    ]
