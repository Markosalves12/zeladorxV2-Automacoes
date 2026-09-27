from django.db import models


class Rotina(models.Model):
    """Uma automação interna (gerar serviços, enviar e-mails...)."""

    CODIGOS = [
        ('gerar_jardinagem', 'Gerar serviços automáticos — Jardinagem'),
        ('gerar_limpeza_predial', 'Gerar serviços automáticos — Limpeza Predial'),
        ('email_resumo_diario', 'E-mail: resumo diário dos gerentes'),
        ('email_atrasados', 'E-mail: serviços atrasados'),
        ('email_concluidos', 'E-mail: serviços concluídos'),
    ]
    FREQUENCIAS = [
        ('diaria', 'Uma vez por dia, a partir do horário'),
        ('continua', 'A cada rodada do agendador'),
    ]

    codigo = models.CharField(max_length=40, choices=CODIGOS, unique=True)
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)
    frequencia = models.CharField(max_length=20, choices=FREQUENCIAS, default='diaria')
    horario = models.TimeField(help_text='Horário mínimo para rodar (rotinas diárias).')
    ordem = models.PositiveSmallIntegerField(default=0)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

    @property
    def ultima_execucao(self):
        return self.execucoes.order_by('-iniciada_em').first()


class Execucao(models.Model):
    STATUS = [
        ('executando', 'Executando'),
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'),
        ('ignorada', 'Ignorada'),
    ]
    ORIGENS = [
        ('agendador', 'Agendador'),
        ('manual', 'Manual (painel)'),
        ('terminal', 'Terminal'),
    ]

    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE, related_name='execucoes')
    data_referencia = models.DateField()
    origem = models.CharField(max_length=20, choices=ORIGENS, default='agendador')
    status = models.CharField(max_length=20, choices=STATUS, default='executando')
    iniciada_em = models.DateTimeField(auto_now_add=True)
    finalizada_em = models.DateTimeField(null=True, blank=True)
    itens_processados = models.PositiveIntegerField(default=0)
    itens_criados = models.PositiveIntegerField(default=0)
    itens_ignorados = models.PositiveIntegerField(default=0)
    detalhes = models.TextField(blank=True)
    executado_por = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['-iniciada_em']
        indexes = [models.Index(fields=['rotina', 'data_referencia', 'status'])]

    def __str__(self):
        return f'{self.rotina} · {self.data_referencia} · {self.get_status_display()}'

    @property
    def duracao(self):
        if self.finalizada_em:
            return self.finalizada_em - self.iniciada_em
        return None
