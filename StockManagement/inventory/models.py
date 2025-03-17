from django.db import models
from productservices.models import Products
from stocklocations.models import Location
from userservices.models import Users
    
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE, related_name='stock_id_products')
    location_id = models.ForeignKey(Location, on_delete = models.CASCADE, related_name='stocklocation')
    signal_qty = models.IntegerField(default=10)
    is_deleted = models.BooleanField(default=False, blank=True,null=True)
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_stock')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_stock')
