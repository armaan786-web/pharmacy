# Generated by Django 4.0.2 on 2022-08-18 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_product_image_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='Image_Url',
            field=models.CharField(max_length=200),
        ),
    ]
