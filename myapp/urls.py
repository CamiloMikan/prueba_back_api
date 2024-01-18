from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'bills', BillViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', UserViewSet.as_view({'post': 'register_user'}), name='register-user'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('export/clients/csv/', export_clients_csv, name='export-clients-csv'),
    path('import/clients/xlsx/', import_from_excel, name='import-from-excel'),
]