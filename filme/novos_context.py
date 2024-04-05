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

    return {'filme_destaque': filme_destaque}

# def link_video(request, episodio):

#     url = episodio.video  # Use o atributo específico do episódio

#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         iframe_element = soup.find('iframe')

#         if iframe_element:
#             link_video = iframe_element['src']
#         else:
#             link_video = '#'  # Ou algum valor padrão caso não haja elemento iframe
#     else:
#         link_video = '#'  # Ou algum valor padrão em caso de erro na solicitação

#     return {'link_video': link_video}