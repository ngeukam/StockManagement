from StockManagement.Helpers import CommonListAPIMixin, CustomPageNumberPagination
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Stock
from .serializers import StockSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Liste et création des stocks    
class StockListAPIView(generics.ListAPIView):
    serializer_class = StockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset=Stock.objects.filter(domain_user_id=self.request.user.domain_user_id.id)
        return queryset
    
    @CommonListAPIMixin.common_list_decorator(StockSerializer)
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)

class StockCreateAPIView(generics.CreateAPIView):
    queryset = Stock.objects.all()  # Will create new Stock objects
    serializer_class = StockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic before saving (if needed)
        serializer.save() 

# Détails d'un stock (lecture, mise à jour et suppression)
class StockRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.filter(is_deleted=False)
    serializer_class = StockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Méthode pour gérer la suppression logique
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class StockForStatAPIView(generics.ListAPIView):
    serializer_class = StockSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    def get_queryset(self):
        queryset = Stock.objects.filter(domain_user_id_id=self.request.user.domain_user_id_id).order_by('-id')
        return queryset