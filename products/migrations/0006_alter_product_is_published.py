# Generated by Django 5.0.2 on 2024-03-06 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options_alter_session_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Opublikowany'),
        ),
    ]
