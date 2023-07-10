from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=150, verbose_name='nome')
    email_comentario = models.EmailField(verbose_name='email')
    comentario = models.TextField(verbose_name='comentário')
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='post')
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='usuario', blank=True,
                                           null=True)
    data_comentario = models.DateTimeField(default=timezone.now, verbose_name='data')
    publicado_comentario = models.BooleanField(default=False, verbose_name='publicado')

    def __str__(self):
        return self.nome_comentario
