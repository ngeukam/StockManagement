from django.urls import path
from .views import PurchaseBillCreateAPIView, PurchaseBillDeleteAPIView, PurchaseBillForStatAPIView, PurchaseBillListAPIView, SaleBillDeleteAPIView, SaleBillForStatAPIView, SaleBillListAPIView, SaleBillRetrieveUpdateDestroyAPIView, SaleCreateAPIView

urlpatterns = [
    # Routes pour les bons de commande
    path('purchase-bills/', PurchaseBillCreateAPIView.as_view(), name='purchase-bill'),
    path('purchase-bills/<int:pk>/', PurchaseBillCreateAPIView.as_view(), name='purchase-bill-detail'),
    path('purchase-list/', PurchaseBillListAPIView.as_view(), name='purchase-bill-list'),
    path('purchase/delete/<int:pk>/', PurchaseBillDeleteAPIView.as_view(), name='purchase-bill-delete'),
    path('purchases/', PurchaseBillForStatAPIView.as_view(), name='purchases'),


     # Route pour lister des factures de vente
    path('sale-bills-list/', SaleBillListAPIView.as_view(), name='sale-bill-list'),
    # Route pour obtenir, modifier ou supprimer une facture de vente
    path('sale-bills/<int:pk>/', SaleBillRetrieveUpdateDestroyAPIView.as_view(), name='sale-bill-detail'),
    # Route pour créer une facture de vente et enregistrer les articles
    path('sale-create/', SaleCreateAPIView.as_view(), name='sale-create'),
    # Route pour supprimer une facture de vente
    path('sale-bills/delete/<int:pk>/', SaleBillDeleteAPIView.as_view(), name='sale-bill-delete'),
    path('sales/', SaleBillForStatAPIView.as_view(), name='sales'),
    
]
