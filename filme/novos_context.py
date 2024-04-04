from .models import Filme
import random

def lista_filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]
    return {"lista_filmes_recentes": lista_filmes}

def lista_filmes_emalta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:8]
    return {"lista_filmes_emalta": lista_filmes}

def filme_destaque(request):
    lista_filmes = []
    filmes_mais_novos = Filme.objects.all().order_by('-data_criacao')[:2]
    filmes_mais_vistos = Filme.objects.all().order_by('-visualizacoes')[:2]
    
    if filmes_mais_novos.exists():
        lista_filmes.extend(filmes_mais_novos)
    if filmes_mais_vistos.exists():
        lista_filmes.extend(filmes_mais_vistos)
    
    if lista_filmes:
        numero_aleatorio = random.randint(0, len(lista_filmes)-1)
        filme_destaque = lista_filmes[numero_aleatorio]
    else:
        filme_destaque = None

    return {'filme_destaque': filme_destaque}
