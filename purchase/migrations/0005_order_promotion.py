# Generated by Django 4.2.5 on 2025-02-07 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0003_alter_promotioncode_options'),
        ('purchase', '0004_alter_order_purchaser_alter_orderdetail_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='promotion', to='promotion.promotioncode'),
        ),
    ]
