from django.db import models
from datetime import date

class OffChainData(models.Model):
    timestamp = models.IntegerField(default=0, primary_key=True)
    priceCoingecko = models.FloatField(default=0)
    last_updated = models.DateField(default=date.today())

    def __str__(self):
        return str(self.timestamp)
    
class OnChainData(models.Model):
    timestamp = models.ForeignKey(OffChainData,on_delete=models.CASCADE,blank=True, null=True)
    priceUniswapV3 = models.FloatField(default=0)
    blockNo = models.IntegerField(default=0)
    last_updated = models.DateField(default=date.today())

    def __str__(self):
        return str(self.timestamp)