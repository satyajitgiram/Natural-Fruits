from django.db import models
from account.models import CustomUser
from django.utils import timezone


class FruitFarmingOption(models.Model):
    title = models.CharField(max_length=200)
    invest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    earn_amount = models.DecimalField(max_digits=10, decimal_places=2)
    per_day_earn = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField()
    icon = models.CharField(max_length=50, null=True, blank=True)  # You can store the icon class or URL here
    description = models.TextField()

    def __str__(self):
        return self.title


class Order(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    item = models.ForeignKey(FruitFarmingOption, on_delete=models.CASCADE)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email + " " + str(self.id)
    