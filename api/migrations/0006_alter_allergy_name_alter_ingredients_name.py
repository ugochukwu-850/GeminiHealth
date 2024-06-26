# Generated by Django 5.0.4 on 2024-04-15 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_medicalprofile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergy',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
