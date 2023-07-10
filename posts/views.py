from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages
# QuerySet = QuerySet é um conjunto de ações que serão realizadas no banco de dados, ou seja, podemos criar, buscar,
# atualizar ou deletar os dados sem escrever a query SQL será executada no banco.
# icontains/iexact = o 'i' significa 'case insensitive', ou seja, que não difere entre letras maiúsculas e minúsculas.


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(numero_comentarios=Count(Case(When(comentario__publicado_comentario=True, then=1))))
        # Conta(Count()) 1(then=1) só no caso(Case())quando(When()) o comentario(comentario__)
        # for publicado(publicado_comentario=True)

        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs
        # A varíavel categoria tá verificando se existe categoria na url, se não existir, retorna o qs normal e para a
        # execução do método por ali
        # ex: /categoria/nada, da pra fazer levantar um erro404
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        # Verifica dentro de categoria_post qual a categoria que quer buscar pelo nome da categoria que seja igual a
        # categoria
        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'

    # If you thus let the function return a dictionary {'foo': 42}, then in your template you can write a variable
    # {{ foo }}, and then it will be replaced with 42. This is frequently used to pass all kinds of data to a
    # template: the user that is logged in, forms, querysets, etc. The template can then render these components
    # accordingly.
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado_comentario=True, post_comentario=post.id)
        contexto['comentarios'] = comentarios

        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post_comentario = post

        if self.request.user.is_authenticated:
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentário enviado com sucesso.')
        return redirect('post_detalhes', pk=post.id)



