from django.db import models
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from gerente.models import Gerente
from areas.models_jardinagem import AreasJardins
from utils.utils import generate_id_random, resize_image
from semana.models import DiasDaSemana
from datetime import timedelta


# Create your models here.
class ServicoJardinagemConfigurado(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Areas = models.ForeignKey(
        to=AreasJardins,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RareaJardinagemconfigurado',
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoJardinagem,
        blank=False,
        null=False,
        related_name='RServicosEscaladosJardinagemServicoConfigurado'
    )

    diasaseremrealizado = models.ManyToManyField(
        to=DiasDaSemana,
        null=False,
        blank=False,
        related_name='Rdiasdasemanaconfiguracoesjardinagem'
    )

    tempomedioplanejado = models.DurationField(
        null=False,
        blank=False,
        default=timedelta(minutes=30)
    )

    horario_1 = models.TimeField(
        null=False,
        blank=False,
    )

    horario_2 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_3 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_4 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_5 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_6 = models.TimeField(
        null=True,
        blank=True,
    )

    horario_7 = models.TimeField(
        null=True,
        blank=True,
    )

    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
    ]

    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Mobilizado'
    )

    def __str__(self):
        servicos_escalados_nomes = ", ".join(servico.nome for servico in self.ServicosEscalados.all())
        return f'{self.Areas} | {servicos_escalados_nomes}'


class ServicoJardinagemAgendado(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    id_configuracao = models.CharField(
        blank=True,
        null=True,
        max_length=20,
    )

    DataDeInicio = models.DateTimeField(
        blank=False,
        null=False,
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoJardinagem,
        blank=False,
        null=False,
        related_name='RServicosEscaladosServicoAgendado'
    )

    ColaboradoresEscalados = models.ManyToManyField(
        to=Gerente,
        blank=False,
        null=False,
        related_name='RColaboradoresEscaladosServicoAgendado',
    )

    ColaboradoresConfirmados = models.ManyToManyField(
        to=Gerente,
        blank=True,
        null=True,
        related_name='RColaboradoresConfirmados'
    )

    ColaboradoresNegados = models.ManyToManyField(
        to=Gerente,
        blank=True,
        null=True,
        related_name='RColaboradoresNegados'
    )

    DescricaoDoServico = models.TextField(
        max_length=200,
        blank=False,
        null=False,
    )

    Areas = models.ForeignKey(
        to=AreasJardins,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='RAreasServicoAgendado'
    )

    status_options = [
        ('Agendado', 'Agendado'),
        ('Cancelado', 'Cancelado'),
        ('Em andamento', 'Em andamento'),
        ('Concluido', 'Concluido')
    ]
    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Agendado'
    )

    foto_solicitacao = models.ImageField(
        upload_to="solicitacao_servico_jardinagem/%Y/%m/%d/",
        blank=True,
        max_length=2000
    )

    foto_entrega = models.ImageField(
        upload_to="entrega_servico_jardinagem/%Y/%m/%d/",
        blank=True,
        max_length=2000
    )

    DataDeConclusao = models.DateTimeField(
        blank=True,
        null=True
    )

    tipo_servico_options = [
        ('Regular', 'Regular'),
        ('Extra', 'Extra'),
        ('Automático', 'Automático'),
    ]

    TipoServico = models.CharField(
        choices=tipo_servico_options,
        null=True,
        blank=True,
        default='Regular',
        max_length=30
    )

    ServicoCompunsivo = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    def save(self, *args, **kwargs):
        if self.foto_solicitacao:
            self.foto_solicitacao = resize_image(self.foto_solicitacao, max_width=500)

        if self.foto_entrega:
            self.foto_entrega = resize_image(self.foto_entrega, max_width=500)

        super(ServicoJardinagemAgendado, self).save(*args, **kwargs)

    def __str__(self):
        colaboradores_nomes = ", ".join(colaborador.username for colaborador in self.ColaboradoresEscalados.all())
        return f'{self.DescricaoDoServico} -- {self.DataDeInicio.strftime("%d/%m/%Y %H:%M")} -- {colaboradores_nomes} '


class FatoServicoJardinagem(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Servico = models.ForeignKey(
        to=ServicoJardinagemAgendado,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="RServicoServicoAgendado"
    )

    data_hora_chegada_na_area = models.DateTimeField(
        blank=False,
        null=False
    )

    data_hora_retorno_area = models.DateTimeField(
        blank=False,
        null=False
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='RColaboradorFatoServico'
    )

    def __str__(self):
        return f'{self.Servico} | {self.data_hora_chegada_na_area} | {self.Gerente}'
