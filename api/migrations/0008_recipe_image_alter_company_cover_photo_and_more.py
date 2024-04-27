# Generated by Django 5.0.4 on 2024-04-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_allergy_classification_allergy_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sdb/user_images/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='sdb/companies/cover'),
        ),
        migrations.AlterField(
            model_name='company',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='sdb/companies/profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='sdb/user_images/'),
        ),
    ]