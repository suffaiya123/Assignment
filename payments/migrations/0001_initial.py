# Generated by Django 3.0 on 2020-09-20 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=50)),
                ('associated_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='cost_price')),
                ('order_status', models.CharField(default='checkout', max_length=50)),
                ('order_created_on', models.DateTimeField()),
                ('order_completed_on', models.DateTimeField(blank=True, default=None, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.Customer')),
            ],
            options={
                'unique_together': {('customer_id',)},
            },
        ),
        migrations.CreateModel(
            name='PayFortCallbackTransactionDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txnid', models.CharField(max_length=100)),
                ('txn_date_time', models.DateTimeField(blank=True, null=True)),
                ('payment_gateway_type', models.CharField(blank=True, max_length=50, null=True)),
                ('mode', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('productInfo', models.CharField(blank=True, max_length=100, null=True)),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('mihpayid', models.CharField(blank=True, max_length=100, null=True)),
                ('bankcode', models.CharField(blank=True, max_length=10, null=True)),
                ('error', models.CharField(blank=True, max_length=50, null=True)),
                ('error_Message', models.CharField(blank=True, max_length=200, null=True)),
                ('bank_ref_num', models.CharField(blank=True, max_length=100, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True)),
                ('additional_charges', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True)),
                ('txn_status_on_payu', models.CharField(blank=True, max_length=20, null=True)),
                ('payu_hash', models.CharField(blank=True, max_length=200, null=True)),
                ('hash_verification_status', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayFortTransactionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('split_info', models.CharField(blank=True, max_length=50, null=True)),
                ('customerName', models.CharField(blank=True, max_length=50, null=True)),
                ('additionalCharges', models.CharField(blank=True, max_length=50, null=True)),
                ('paymentMode', models.CharField(blank=True, max_length=20, null=True)),
                ('hash', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('error_Message', models.CharField(blank=True, max_length=200, null=True)),
                ('paymentId', models.CharField(blank=True, max_length=50, null=True)),
                ('productInfo', models.CharField(blank=True, max_length=100, null=True)),
                ('customerEmail', models.CharField(blank=True, max_length=50, null=True)),
                ('customerPhone', models.CharField(blank=True, max_length=15, null=True)),
                ('merchantTransactionId', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('notificationId', models.CharField(blank=True, max_length=50, null=True)),
                ('hash_verification_status', models.CharField(blank=True, max_length=50, null=True)),
                ('response_date', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayFortTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=20, unique=True)),
                ('transaction_id', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='cost_price')),
                ('order_status', models.CharField(default='initiated', max_length=50)),
                ('Transaction_date', models.DateTimeField()),
                ('date_recieved_on', models.DateTimeField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyUserTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50)),
                ('paytm_user', models.CharField(max_length=15)),
                ('verification_status', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.Order')),
            ],
            options={
                'unique_together': {('order', 'transaction_id')},
            },
        ),
    ]
