from rest_framework import viewsets, status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from .models import *
from .seriealizers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
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

class ClientRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['post'])
    def register_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'Usuario registrado con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
    
    
def export_clients_csv(request,):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename= clients.csv"

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
@permission_classes([AllowAny])
def import_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('pruebas_api')

        # Comprueba si el archivo es un archivo CSV
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'El archivo no es de tipo CSV.'}, status=400)

        try:
            success_count = 0
            error_count = 0
            errors = []

            # Convertir el contenido del InMemoryUploadedFile a texto
            csv_content = csv_file.read().decode('utf-8').splitlines()

            # Crear el lector CSV
            csv_reader = csv.reader(csv_content, delimiter=';')

            # Saltar la primera fila si es una cabecera
            header = next(csv_reader, None)

            for row in csv_reader:
                try:
                    # Tratar de desempaquetar cinco valores
                    document, first_name, last_name, email, password = row[:5]

                    Clients.objects.create(
                        document=document,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password
                    )
                    success_count += 1
                except (ValueError, IndexError) as e:
                    # Manejar errores si no hay suficientes valores en la fila
                    error_count += 1
                    errors.append({'row_data': row, 'error_message': str(e)})

            response_data = {
                'success_count': success_count,
                'error_count': error_count,
                'errors': errors
            }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': f'Error durante la importación: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
