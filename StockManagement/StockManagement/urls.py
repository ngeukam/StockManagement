"""
URL configuration for StockManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from userservices.Controller.SuperAdminDynamicFormController import SuperAdminDynamicFormController
from userservices.Controller.DynamicFormController import DynamicFormController
from userservices.Controller.SidebarController import ModuleUrlsListAPIView, ModuleView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('userservices.urls')),
    path('api/v1/stocklocations/', include('stocklocations.urls')),
    path('api/v1/transactions/', include('transactions.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/products/', include('productservices.urls')),
    path('api/v1/getMenus/',ModuleView.as_view(),name='sidebarmenu'),
    path('api/v1/getForm/<str:modelName>/',DynamicFormController.as_view(),name='dynamicForm'),
    path('api/v1/getForm/<str:modelName>/<str:id>/',DynamicFormController.as_view(),name='dynamicForm'),
    path('api/v1/superAdminForm/<str:modelName>/',SuperAdminDynamicFormController.as_view(),name='superadmindynamicForm'),
    path('api/v1/moduleUrls/',ModuleUrlsListAPIView.as_view(),name='moduleUrls_superadmin'),
]
