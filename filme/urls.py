from django.urls import path, include
from .views import Homepage, HomeFilmes, DetalhesFilme, TelaEpisodio, PesquisaFilme

app_name = 'filme'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', HomeFilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', DetalhesFilme.as_view(), name='detalhesfilme'),
    path('filmes/<int:pk>/<int:epk>', TelaEpisodio.as_view(), name='telaepisodio'),
    path('pesquisa/', PesquisaFilme.as_view(), name='pesquisafilmes'),
]