# Generated by Django 3.0 on 2020-09-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='order_no',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_completed_on',
            new_name='recieved_amount_date',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_created_on',
            new_name='transaction_date',
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_text',
            field=models.TextField(default=None, max_length=125),
        ),
    ]
