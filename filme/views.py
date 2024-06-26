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

        url_link_video = self.enviar_url_para_vm(episodio.video)
        context['url_link_video'] = url_link_video


        return context

    def enviar_url_para_vm(url):
        vm_url = 'http://34.95.209.181/processar-url'
        payload = {'url': url}
        response = requests.post(vm_url, json=payload)
        return response.json()['url_processada']


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