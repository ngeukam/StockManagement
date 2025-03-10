from StockManagement.Helpers import CommonListAPIMixin, CommonListAPIMixinWithFilter, CustomPageNumberPagination, getDynamicFormFields, renderResponse
from productservices.models import Products
from rest_framework import generics, status, serializers
from inventory.models import Stock
from userservices.models import Users
from .models import PurchaseBillDetails, PurchaseItem, PurchaseBill, SaleBillDetails
from .serializers import PurchaseItemSerializer, PurchaseBillSerializer, SaleBillDetailsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from .models import SaleBill, SaleItem
from .serializers import SaleBillSerializer, SaleItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction


# Détails d'un bon de commande (PurchaseBill)
class PurchaseBillCreateAPIView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):  
                # Vérifie que pk est un entier
        if pk is not None and not isinstance(pk, int):
            try:
                pk = int(pk)  # Convertit en entier si possible
            except ValueError:
                return Response({"error": "Invalid bill ID format"}, status=400)

        # Récupération de la facture
        po = PurchaseBill.objects.filter(
            domain_user_id=request.user.domain_user_id.id, 
            billno=pk
        ).first() if pk else PurchaseBill()  

        # Récupération des articles liés
        poItems = PurchaseItem.objects.filter(billno=pk) if pk else []
        poItems = PurchaseItemSerializer(poItems, many=True).data
        # Gestion des données du fournisseur
        poData = {
            'supplier_id': po.supplier_id.id,
            'supplier_email': po.supplier_id.email
        } if po and po.supplier_id else {}

        # Récupération des champs dynamiques
        poFields = getDynamicFormFields(po if po else PurchaseBill(), request.user.domain_user_id.id, skip_related=['supplier_id'], skip_fields=[])
        poItemFields = getDynamicFormFields(PurchaseItem(), request.user.domain_user_id.id, skip_related=['product'], skip_fields=[])

        return renderResponse(
            data={
                'poData': poData,
                'poItems': poItems,
                'poFields': poFields,
                'poItemFields': poItemFields
            },
            message='Purchase Order Fields',
            status=200
        )


    
    def post(self, request, *args, **kwargs):
        """
        Create a new purchase bill along with the purchase items and update stock.
        """
        supplier_id = request.data.get('supplier_id')
        supplier = get_object_or_404(Users, pk=supplier_id)

        domain_user = request.user.domain_user_id  # Directement depuis request.user
        created_by_user = request.user
        updated_by_user = request.user

        with transaction.atomic():
            # Créer une nouvelle facture d'achat
            purchase_bill = PurchaseBill(
                supplier_id=supplier,
                domain_user_id=domain_user,
                created_by_user_id=created_by_user,
                updated_by_user_id=updated_by_user
            )
            purchase_bill.save()

            # Récupérer les items de la requête
            items_data = request.data.get('items', [])

            # Traiter chaque item
            for item_data in items_data:
                if 'quantity_ordered' not in item_data:
                    raise serializers.ValidationError({"quantity_ordered": "This field is required."})

                item_data['billno'] = purchase_bill.billno
                purchase_item_serializer = PurchaseItemSerializer(data=item_data)

                if not purchase_item_serializer.is_valid():
                    raise serializers.ValidationError(purchase_item_serializer.errors)
                purchase_item = purchase_item_serializer.save()
                # Enregistrer PurchaseBillDetails (si nécessaire)
                purchasebilldetailsobj = PurchaseBillDetails(billno=purchase_bill)
                purchasebilldetailsobj.save()
                # Mettre à jour le stock
                stock = get_object_or_404(Stock, product_id=item_data['product_id'])
                
                stock.quantity += int(purchase_item.quantity)
                stock.save()

            # Retourner une réponse
        return Response({
            'message': 'Purchase bill and items have been created successfully.',
            'purchaseBill': PurchaseBillSerializer(purchase_bill).data
        }, status=status.HTTP_201_CREATED)

# Liste des bons de commande (PurchaseBill)
class PurchaseBillListAPIView(generics.ListAPIView):
    serializer_class = PurchaseBillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        queryset = PurchaseBill.objects.prefetch_related('purchasebillno', 'purchasedetailsbillno').filter(domain_user_id_id=self.request.user.domain_user_id_id).order_by('-billno')
        return queryset

# Supprimer une facture d'achat et restaurer les articles au stock
class PurchaseBillDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            purchase_bill = PurchaseBill.objects.get(billno=pk)
            items = PurchaseItem.objects.filter(billno=purchase_bill.billno)

            # Restaurer les articles au stock
            for item in items:
                stock = Stock.objects.get(product_id=item.product_id.id)
                stock.quantity += item.quantity
                stock.save()

            # Supprimer la facture de vente
            purchase_bill.delete()

            return Response({'status': 'Purchase bill deleted successfully'}, status=200)

        except SaleBill.DoesNotExist:
            return Response({'error': 'Purchase bill not found'}, status=404)
        
# Liste et création des factures de vente
class SaleBillListAPIView(generics.ListAPIView):
    serializer_class = SaleBillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        queryset = SaleBill.objects.prefetch_related('salebillno', 'saledetailsbillno').filter(domain_user_id_id=self.request.user.domain_user_id_id).order_by('-billno')
        return queryset
    

# Détails d'une facture de vente (consultation, modification, suppression)
class SaleBillRetrieveUpdateDestroyAPIView(generics.RetrieveAPIView):
    queryset = SaleBill.objects.all()
    serializer_class = SaleBillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

# Créer une facture de vente et enregistrer les articles
class SaleCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer tous les stocks disponibles
        stocks = Stock.objects.filter(is_deleted=False)
        return Response({'stocks': stocks})


    def post(self, request):
        # Récupérer les données de la facture et des articles
        bill_data = request.data.get('bill', {})
        items_data = request.data.get('items', [])

        if not items_data:
            return Response({"error": "No items provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier les doublons et la validité des quantités
        seen_products = set()
        product_ids = [item['product'] for item in items_data if 'product' in item]
        products = Products.objects.in_bulk(product_ids)  # Charge tous les produits en une seule requête

        for item in items_data:
            product_id = item.get('product')
            productdisplay = products.get(product_id)

            if not productdisplay:
                return Response({"error": f"Product with ID {product_id} not found."}, status=status.HTTP_400_BAD_REQUEST)

            if product_id in seen_products:
                return Response({"error": f"The product {productdisplay.name} appears more than once."}, status=status.HTTP_400_BAD_REQUEST)
            seen_products.add(product_id)

            # Vérifier que la quantité n'est pas égale à 0
            if int(item.get('quantity', 0)) == 0:
                return Response({"error": f"The quantity for product {productdisplay.name} cannot be 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer les stocks en une seule requête
        stocks = Stock.objects.select_for_update().in_bulk(product_ids)

        with transaction.atomic():
            # Créer la facture de vente
            sale_bill_serializer = SaleBillSerializer(data=bill_data)
            if not sale_bill_serializer.is_valid():
                return Response(sale_bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            domain_user = request.user.domain_user_id  # Directement depuis request.user
            created_by_user = request.user
            sale_bill = sale_bill_serializer.save(
                created_by_user_id=created_by_user, 
                domain_user_id=domain_user
            )
            # Parcourir les articles
            for item_data in items_data:
                product_id = item_data['product']
                productdisplay = products[product_id]

                item_data['billno'] = sale_bill.billno  # Associer l'article à la facture
                item_data['domain_user_id'] = request.user.domain_user_id_id
                item_data['created_by_user_id'] = request.user.id

                sale_item_serializer = SaleItemSerializer(data=item_data)
                billdetailsobj = SaleBillDetails(billno=sale_bill)
                billdetailsobj.save()

                if not sale_item_serializer.is_valid():
                    raise serializers.ValidationError(sale_item_serializer.errors)

                # Vérification du stock avant enregistrement
                stock = stocks.get(product_id)
                if not stock:
                    raise serializers.ValidationError({"error": f"Product {productdisplay.name} not found in stock."})

                if stock.quantity < int(item_data['quantity']):
                    raise serializers.ValidationError({"error": f"Insufficient stock for product {productdisplay.name}."})

                # Déduction du stock et enregistrement de l'article
                stock.quantity -= int(item_data['quantity'])
                stock.save()
                sale_item_serializer.save()
        return Response({'message': "Sale bill and items created successfully.", "error":False}, status=status.HTTP_201_CREATED)


# Supprimer une facture de vente et restaurer les articles au stock
class SaleBillDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            sale_bill = SaleBill.objects.get(billno=pk)
            items = SaleItem.objects.filter(billno=sale_bill.billno)

            # Restaurer les articles au stock
            for item in items:
                stock = Stock.objects.get(product_id=item.product.id)
                stock.quantity += item.quantity
                stock.save()

            # Supprimer la facture de vente
            sale_bill.delete()

            return Response({'status': 'Sale bill deleted successfully'}, status=200)

        except SaleBill.DoesNotExist:
            return Response({'error': 'Sale bill not found'}, status=404)


class PurchaseBillForStatAPIView(generics.ListAPIView):
    serializer_class = PurchaseBillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        queryset = PurchaseBill.objects.prefetch_related('purchasebillno', 'purchasedetailsbillno').filter(domain_user_id_id=self.request.user.domain_user_id_id).order_by('-billno')[:2]
        return queryset

class SaleBillForStatAPIView(generics.ListAPIView):
    serializer_class = SaleBillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    def get_queryset(self):
        queryset = SaleBill.objects.prefetch_related('salebillno', 'saledetailsbillno').filter(domain_user_id_id=self.request.user.domain_user_id_id).order_by('-billno')[:2]
        return queryset