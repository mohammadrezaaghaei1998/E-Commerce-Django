# Generated by Django 4.2.4 on 2023-08-08 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_userinformation_card_cvv_userinformation_card_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='cart_item',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cartitem'),
        ),
    ]