from django.urls import path, include
from .views import Homepage, HomeFilmes, DetalhesFilme, TelaEpisodio, PesquisaFilme, PaginaPerfil, CriarConta
from django.contrib.auth import views as AuthView

app_name = 'filme'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', HomeFilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>', DetalhesFilme.as_view(), name='detalhesfilme'),
    path('filmes/<int:pk>/<int:epk>', TelaEpisodio.as_view(), name='telaepisodio'),
    path('pesquisa/', PesquisaFilme.as_view(), name='pesquisafilmes'),
    path('login/', AuthView.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', AuthView.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('editarperfil/', PaginaPerfil.as_view(), name='editarperfil'),
    path('criarconta/', CriarConta.as_view(), name='criarconta'),
]