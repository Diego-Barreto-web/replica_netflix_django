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
    filme = Filme.objects
    filmes_mais_novos = filme.all().order_by('-data_criacao')[:2]
    filmes_mais_vistos = filme.all().order_by('-visualizacoes')[:2]
    
    if len(filmes_mais_novos) > 0:
        for filme in filmes_mais_novos:
            lista_filmes.append(filme)
    if len(filmes_mais_vistos) > 0:
        for filme in filmes_mais_vistos:
            lista_filmes.append(filme)
    numero_aleatorio = random.randint(0, len(lista_filmes)-1)

    return {'filme_destaque':lista_filmes[numero_aleatorio]}
