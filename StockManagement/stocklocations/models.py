from django.db import models

from userservices.models import Users

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=55)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_location')
    added_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='added_by_user_id_location')


    # Ensure the combination of name and address is unique
    class Meta:
        unique_together = ('name', 'address')

    def __str__(self):
        return "Stock location: " + self.name + ", " + self.address
    
    def defaultkey():
        return "name"
