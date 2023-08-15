# Generated by Django 4.2.4 on 2023-08-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_userinformation_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='phone_number',
            field=models.PositiveIntegerField(default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='zipcode',
            field=models.PositiveIntegerField(default=0, max_length=10),
        ),
    ]