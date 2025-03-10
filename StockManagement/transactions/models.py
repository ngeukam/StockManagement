from django.db import models
from inventory.models import Stock
from productservices.models import Products
from userservices.models import Users


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier_id = models.ForeignKey(Users, on_delete = models.CASCADE, blank=True,null=True, related_name='purchasesupplier')
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_purchase_order')
    payment_terms=models.CharField(max_length=255,choices=[('CASH','CASH'),('CREDIT','CREDIT'),('ONLINE','ONLINE'),('CHEQUE','CHEQUE')],default='CASH')
    payment_status=models.CharField(max_length=255,choices=[('PAID','PAID'),('UNPAID','UNPAID'),('PARTIAL PAID','PARTIAL PAID'),('CANCELLED','CANCELLED')],default='UNPAID')
    status=models.CharField(max_length=255,choices=[('DRAFT','DRAFT'), ('CREATED','CREATED'), ('APPROVED','APPROVED'),('SENT','SENT'),('RECEIVED','RECEIVED'),('PARTIAL RECEIVED','PARTIAL RECEIVED'),('CANCELLED','CANCELLED'),('RETURNED','RETURNED'),('COMPLETE','COMPLETE')],default='DRAFT')
    created_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='created_by_user_id_purchase_order')
    updated_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='updated_by_user_id_purchase_order')
    approved_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='approved_by_user_id_purchase_order')
    approved_at=models.DateTimeField(null=True,blank=True)
    cancelled_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='cancelled_by_user_id_purchase_order')
    cancelled_at=models.DateTimeField(null=True,blank=True)
    cancelled_reason=models.TextField(null=True,blank=True)
    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.quantity * item.buying_price
        return total

#contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno', blank=True, null=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_id_purchase_bill_items')
    quantity = models.IntegerField(default=0)
    buying_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    selling_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.product_id.name

#contains the other details in the purchases bill
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasedetailsbillno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)


#contains the sale bills made
class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_sale_bill')
    created_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='created_by_user_id_sale_bill')


    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
        
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        for item in saleitems:
            total += item.total_price
        return total

#contains the sale stocks made
class SaleItem(models.Model):
    quantity = models.IntegerField(default=1)
    billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='salebillno')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='saleitem')
    domain_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='domain_user_id_sale_bill_item')
    created_by_user_id=models.ForeignKey(Users,on_delete=models.CASCADE,blank=True,null=True,related_name='created_by_user_id_sale_bill_item')

    @property
    def total_price(self):
        if self.product is not None:
            return self.quantity * self.product.initial_selling_price
        return 0  

    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.product.name


#contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno')
    
    eway = models.CharField(max_length=50, blank=True, null=True)    
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)
