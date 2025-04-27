from django.shortcuts import render
import requests
from django.http import JsonResponse
from .serializers import ItemSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Item


#consumir api con frontend
def index(request):
    Pokemon = None
    if request.method == 'POST':
        pokemon_name = request.POST.get('Pokemon')
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
        if response.status_code == 200:
            Pokemon = response.json()
    return render(request, 'index.html', {'Pokemon': Pokemon})

#consumir api con backend
def recurso_view(request):
    try:
        response = requests.get('https://api.chucknorris.io/jokes/random')
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        data = response.json()

        return JsonResponse(data)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


#para crear un endpoint que permita crear varios items a la vez usar '/api/items/bulk-create/'
#para crear un endpoint que permita un item a la vez usar '/api/items/'
    
class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    #permite que se cambie el nombre de la url a '/api/items/bulk-create/' para crear varios items a la vez
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """
        Endpoint para crear múltiples items en una sola solicitud.
        """
        # Verifica que el cuerpo de la solicitud sea una lista
        if not isinstance(request.data, list):
            return Response(
                {"error": "Se esperaba una lista de objetos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Inicializa el serializer con many=True
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Guarda los objetos en la base de datos
        return Response(serializer.data, status=status.HTTP_201_CREATED)