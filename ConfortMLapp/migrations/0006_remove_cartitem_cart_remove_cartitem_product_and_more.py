# Generated by Django 4.2 on 2024-05-30 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ConfortMLapp', '0005_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
