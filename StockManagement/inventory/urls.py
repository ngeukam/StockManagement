from django.urls import path
from . import views

urlpatterns = [
    # Liste des stocks et création de stocks
    path('stocks/', views.StockListAPIView.as_view(), name='stock-list'),  # List view
    path('stocks/create/', views.StockCreateAPIView.as_view(), name='stock-create'),  # Create view
    path('stocks-stat/', views.StockForStatAPIView.as_view(), name='stock-stat'),  # List view


    # Détails d'un stock spécifique (consultation, mise à jour, suppression)
    path('stocks/<int:pk>/', views.StockRetrieveUpdateDestroyAPIView.as_view(), name='stock-detail'),
]