from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action,api_view,parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .models import *
from .seriealizers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .resources import ClientResource
import csv

class JWTAuthenticationMixin:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ClientViewSet(JWTAuthenticationMixin, viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer

class BillViewSet(JWTAuthenticationMixin, viewsets.ModelViewSet):
    queryset = Bills.objects.all()
    serializer_class = BillSerializer

class ProductViewSet(JWTAuthenticationMixin, viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'Usuario registrado con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

token_obtain_pair = MyTokenObtainPairView.as_view()

def export_clients_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename='clients.csv'"

    # Obtener todos los clientes con la cantidad de facturas relacionadas
    clients = Clients.objects.annotate(num_bills=models.Count('bills'))

    # Crear el objeto de escritura CSV
    writer = csv.writer(response)
    
    # Escribir la cabecera del CSV
    writer.writerow(['Documento', 'Nombre Completo', 'Cantidad de Facturas'])

    # Escribir los datos de cada cliente
    for client in clients:
        writer.writerow([client.document, client.full_name(), client.num_bills])

    return response

@api_view(['POST'])
@parser_classes([FileUploadParser])
def import_clients_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "No se proporcionó el archivo CSV"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ClientImportSerializer(data=request.data)

    if serializer.is_valid():
        try:
            file = serializer.validated_data['file']
            resource = ClientResource()
            dataset = resource.load(file.read().decode('utf-8'), format='csv')

            if dataset.headers:
                mapping = {
                    'Documento': 'document',
                    'Nombre': 'first_name',
                    'Apellido': 'last_name',
                    'Email': 'email',
                    'Contraseña': 'password',
                }

                resource.import_data(dataset, dry_run=False, mapping=mapping)

                for row in dataset.dict:
                    client = Clients(
                        document=row['Documento'],
                        first_name=row['Nombre'],
                        last_name=row['Apellido'],
                        email=row['Email'],
                        password=row['Contraseña']
                    )
                    client.save()

                return Response({"message": "Importación exitosa"})
            else:
                return Response({"error": "El archivo CSV debe tener encabezados"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error en la importación: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": f"Datos no válidos: {serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
