# Generated by Django 5.0.6 on 2024-06-03 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0015_women_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]