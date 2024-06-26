# Generated by Django 5.0.4 on 2024-04-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_allergy_name_alter_ingredients_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergy',
            name='classification',
            field=models.CharField(default=1, max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allergy',
            name='group',
            field=models.CharField(default=1, max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allergy',
            name='topology',
            field=models.CharField(default=1, max_length=225),
            preserve_default=False,
        ),
    ]
