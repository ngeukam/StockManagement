from django.urls import path
from .views import LocationListAPIView, LocationDetail, LocationCreateAPIView

urlpatterns = [
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('location/create/', LocationCreateAPIView.as_view(), name='location-create'),
    path('locations/<int:pk>/', LocationDetail.as_view(), name='location-detail'),
]
