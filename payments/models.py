from django.db import models
from users.models import Users
# Create your models here.


class Customer(models.Model):
    customer_id = models.CharField(max_length=50)
    associated_user = models.OneToOneField(Users, on_delete=models.CASCADE)

    objects = models.Manager()


class Order(models.Model):
    order_no = models.CharField(max_length=10, editable=False, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=7, verbose_name='cost_price')
    order_status = models.CharField(max_length=50, default='checkout')
    transaction_date = models.DateTimeField()
    recieved_amount_date = models.DateTimeField(default=None, null=True, blank=True)
    transaction_text = models.TextField(max_length=125, default=None)
    objects = models.Manager()

    class Meta:
        unique_together = ('customer_id',)


