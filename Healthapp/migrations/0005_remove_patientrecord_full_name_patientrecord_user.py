# Generated by Django 4.1.5 on 2023-08-17 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Healthapp', '0004_patientrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientrecord',
            name='Full_name',
        ),
        migrations.AddField(
            model_name='patientrecord',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Healthapp.customuser'),
            preserve_default=False,
        ),
    ]