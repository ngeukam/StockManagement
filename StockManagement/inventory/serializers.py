from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    product_id=serializers.SerializerMethodField()
    location_id=serializers.SerializerMethodField()
    domain_user_id=serializers.SerializerMethodField()
    added_by_user_id=serializers.SerializerMethodField()
    class Meta:
        model = Stock
        fields = '__all__'
    
    def get_product_id(self,obj):
        return "#"+str(obj.product_id.id)+" "+obj.product_id.name
    
    def get_location_id(self,obj):
        return "#"+str(obj.location_id.id)+" "+obj.location_id.name+", "+obj.location_id.address
    
    def get_domain_user_id(self,obj):
        return "#"+str(obj.domain_user_id.id)+" "+obj.domain_user_id.username
    
    def get_added_by_user_id(self,obj):
        return "#"+str(obj.added_by_user_id.id)+" "+obj.added_by_user_id.username
