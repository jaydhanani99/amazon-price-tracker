# Generated by Django 2.1.15 on 2021-02-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_product_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='email',
            field=models.TextField(),
        ),
    ]
