from decimal import Decimal

from django.db import models

# Create your models here.


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_package = models.CharField(max_length=100)
    service_tax = models.DecimalField(max_digits=50, decimal_places=2)
    service_image = models.ImageField(upload_to='services/')
    active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        self.service_tax = self.service_price * Decimal('0.18')
        super(Service, self).save(*args, **kwargs)

    @property
    def total_price(self):
        return self.service_price + self.service_tax