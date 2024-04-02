from typing import Any
from django.shortcuts import render
from .models import Filme, Episodio
from django.views.generic import TemplateView, ListView, DetailView

class Homepage(TemplateView):
    template_name = 'homepage.html'

class Homefilmes(ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # retorna object_list -> lista de itens do modelo

class DetalhesFilme(DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object -> 1 item do modelo

    def get(self, request, *args, **kwargs):
        total_visualizacao_episodios = 0
        filme = self.get_object()

        for episodio in filme.episodios.all():
            total_visualizacao_episodios += episodio.visualizacoes
        filme.visualizacoes = total_visualizacao_episodios
        filme.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context
    
class TelaEpisodio(DetailView):
    template_name = 'telaepisodio.html'    
    model = Episodio

    def get(self, request, *args, **kwargs):
        episodio_id = self.kwargs['epk']
        episodio = Episodio.objects.get(id=episodio_id)
        episodio.visualizacoes += 1
        episodio.save()
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        episodio_id = self.kwargs['epk']
        episodio = Episodio.objects.get(id=episodio_id)
        context['episodio'] = episodio

        return context

# Create your views here.
# def homepage(request):
#     return render(request, "homepage.html")
    
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)