from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Filme, Episodio
from django.views.generic import TemplateView, ListView, DetailView

class Homepage(TemplateView):
    template_name = 'homepage.html'

class HomeFilmes(ListView):
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

        usuario = request.user
        usuario.filmes_vistos.add(episodio.filme)
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        episodio_id = self.kwargs['epk']
        episodio = Episodio.objects.get(id=episodio_id)
        context['episodio'] = episodio

        return context

class PesquisaFilme(ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None
        
