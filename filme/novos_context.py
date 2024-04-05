from .models import Filme, Episodio
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
        for filme_novo in filmes_mais_novos:
            lista_filmes.append(filme_novo)
    if filmes_mais_vistos.exists():
        for filme_visto in filmes_mais_vistos:
            lista_filmes.append(filme_visto)
    
    if lista_filmes:
        numero_aleatorio = random.randint(0, len(lista_filmes)-1)
        filme_destaque = lista_filmes[numero_aleatorio]
    else:
        filme_destaque = None

    for film in lista_filmes:
        print(film)
    return {'filme_destaque': filme_destaque}

def link_video(request):
    import requests
    from bs4 import BeautifulSoup

    url = Episodio.video

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        iframe_element = soup.find('iframe')

        if iframe_element:
            video_link = iframe_element['src']
        else:
            video_link = iframe_element['#']
    else:
        video_link = iframe_element['#']

    return {'video_link': video_link}