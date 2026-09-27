from django.conf import settings
from django.db import models


class NotificacaoEnviada(models.Model):
    """Registro de cada e-mail. A `chave` única impede envio duplicado."""

    TIPOS = [
        ('resumo_diario', 'Resumo diário'),
        ('atrasado', 'Serviço atrasado'),
        ('concluido', 'Serviço concluído'),
        ('teste', 'E-mail de teste'),
    ]
    STATUS = [
        ('enviado', 'Enviado'),
        ('falhou', 'Falhou'),
    ]

    chave = models.CharField(max_length=180, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPOS)
    status = models.CharField(max_length=20, choices=STATUS, default='enviado')
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='notificacoes_ops',
    )
    email = models.EmailField(max_length=150)
    assunto = models.CharField(max_length=200)
    referencia = models.CharField(max_length=40, blank=True, help_text='id_random do serviço, quando houver')
    setor = models.CharField(max_length=30, blank=True)
    erro = models.TextField(blank=True)
    tentativas = models.PositiveSmallIntegerField(default=1)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criada_em']
        indexes = [models.Index(fields=['tipo', 'status', 'criada_em'])]

    def __str__(self):
        return f'{self.get_tipo_display()} → {self.email}'


class PreferenciaNotificacao(models.Model):
    """Permite desligar tipos de e-mail para um gerente específico."""

    gerente = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferencia_notificacao_ops',
    )
    receber_resumo_diario = models.BooleanField(default=True)
    receber_atrasados = models.BooleanField(default=True)
    receber_concluidos = models.BooleanField(default=True)

    def __str__(self):
        return f'Preferências de {self.gerente}'
