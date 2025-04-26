from django.shortcuts import render
import requests
from django.http import JsonResponse


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