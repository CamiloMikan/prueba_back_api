from import_export import resources
from .models import Clients

class ClientResource(resources.ModelResource):
    class Meta:
        model = Clients
        fields = ('document', 'first_name', 'last_name', 'email', 'password')
