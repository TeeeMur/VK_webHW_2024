# Generated by Django 5.1.3 on 2024-11-10 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkHWApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='reference_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vkHWApp.question'),
        ),
    ]
