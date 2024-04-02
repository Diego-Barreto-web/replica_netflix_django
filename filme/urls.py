from django.urls import path, include
from .views import Homepage, Homefilmes, DetalhesFilme, TelaEpisodio

app_name = 'filme'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', DetalhesFilme.as_view(), name='detalhesfilme'),
    path('filmes/<int:pk>/<int:epk>', TelaEpisodio.as_view(), name='telaepisodio'),
]