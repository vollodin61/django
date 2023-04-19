# Generated by Django 4.2 on 2023-04-17 18:47

from django.db import migrations, models
import shopapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0010_order_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='preview',
            field=models.ImageField(blank=True, null=True,
                                    upload_to=shopapp.models.product_preview_directory_path),
        ),
    ]