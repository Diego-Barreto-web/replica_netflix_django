from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, redirect, reverse
from .models import Filme, Episodio, Usuario
from .forms import CriarContaForm, FormHomePage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from bs4 import BeautifulSoup

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)
        
    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # retorna object_list -> lista de itens do modelo

class DetalhesFilme(LoginRequiredMixin, DetailView):
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
    
class TelaEpisodio(LoginRequiredMixin, DetailView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodio_id = self.kwargs['epk']
        episodio = Episodio.objects.get(id=episodio_id)
        context['episodio'] = episodio

        # Chamando a função link_video para obter o link do vídeo
        context['link_video'] = self.link_video(episodio)

        print(self.link_video(episodio) + 'teste03')

        return context

    # Definindo a função link_video fora da classe TelaEpisodio
    def link_video(self, episodio):
        url = episodio.video
        print(url + 'teste01')

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        iframe_element = soup.find('iframe')
        print(soup + 't4')
        print(iframe_element + 'teste02')

        if iframe_element:
            return iframe_element['src']
        else:
            return '#'

class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None
        
class PaginaPerfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class CriarConta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('filme:login')