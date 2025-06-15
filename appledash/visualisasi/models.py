
from django.db import models

class AppleSales(models.Model):
    state = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    iphone_sales = models.FloatField()
    ipad_sales = models.FloatField()
    mac_sales = models.FloatField()
    wearables = models.FloatField()
    services_revenue = models.FloatField()

    def __str__(self):
        return f"{self.state}, {self.region}"
