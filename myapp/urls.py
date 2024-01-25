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
    path('register/', ClientRegistrationView.as_view(), name='client-registration'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('export/clients/csv/', export_clients_csv, name='export-clients-csv'),
    path('import/clients/xlsx/', import_from_excel, name='import-from-excel'),
]