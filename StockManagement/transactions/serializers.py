from rest_framework import serializers
from .models import PurchaseBill, PurchaseItem, PurchaseBillDetails, SaleItem, SaleBillDetails, SaleBill


class PurchaseItemSerializer(serializers.ModelSerializer):
    product_id_name = serializers.CharField(source='product_id.name', read_only=True)
    sku = serializers.CharField(source='product_id.sku', read_only=True)
    class Meta:
        model = PurchaseItem
        fields = '__all__'

class PurchaseBillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseBillDetails
        fields = '__all__'

class PurchaseBillSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True, source='purchasebillno')  # Use correct source
    details = PurchaseBillDetailsSerializer(many=True, read_only=True, source='purchasedetailsbillno')
    supplier_id=serializers.CharField(source='supplier_id.email',read_only=True)
    supplier_name=serializers.CharField(source='supplier_id.username',read_only=True)
    created_by_user_id=serializers.CharField(source='created_by_user_id.username',read_only=True)
    domain_user_id=serializers.CharField(source='domain_user_id.username',read_only=True)
    class Meta:
        model = PurchaseBill
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = SaleItem
        fields = ['quantity', 'billno', 'product', 'product_name', 'total_price', 'domain_user_id', 'created_by_user_id']

    def get_total_price(self, obj):
        # Retourner le total calculé
        return obj.total_price

class SaleBillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleBillDetails
        fields = '__all__'

class SaleBillSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True, source='salebillno')  # Use correct source
    details = SaleBillDetailsSerializer(many=True, read_only=True, source='saledetailsbillno')
    class Meta:
        model = SaleBill
        fields = '__all__'

