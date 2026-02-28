from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.views import InventarioListView, InventarioDetailView, CategoriaListView, CategoriaDetailView
from cuentas.views import UsuarioViewSet
from tienda.views import CompraViewSet, VentaViewSet

router = DefaultRouter()
router.register('usuario', UsuarioViewSet, basename='usuarios'),
router.register('compra', CompraViewSet, basename='compra'),
router.register('venta', VentaViewSet, basename='venta'),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='refresh token'),
    path('api/categoria/', CategoriaListView.as_view(), name="categoria"),
    path('api/categoria/<int:pk>/', CategoriaDetailView.as_view(), name="categoria-detalle"),
    path('api/inventario/', InventarioListView.as_view(), name="inventario"),
    path('api/inventario/<int:pk>/', InventarioDetailView.as_view(), name="inventario-detalle"),
    path('api/', include(router.urls)),
]