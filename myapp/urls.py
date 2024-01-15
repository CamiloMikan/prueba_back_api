# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'bills', BillViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', UserViewSet.as_view({'post': 'register_user'}), name='register-user'),
    path('token/', token_obtain_pair, name='token-obtain-pair'),
    path('export/clients/csv/', export_clients_csv, name='export-clients-csv'),
    path('import/clients/csv/', import_clients_csv, name='import-clients-csv'),
]
