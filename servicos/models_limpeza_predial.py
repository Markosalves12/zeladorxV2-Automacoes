from django.db import models
from utils.utils import generate_id_random
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from areas.models_limpeza_predial import AreaLimpezaPredial
from datetime import timedelta
from semana.models import DiasDaSemana
from gerente.models import Gerente
from utils.utils import resize_image


class ServicoLimpezaPredialConfigurado(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Areas = models.ForeignKey(
        to=AreaLimpezaPredial,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='Rarealimpezapredialconfigurado',
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        related_name='RServicosEscaladosLimpezaPredialServicoConfigurado'
    )

    diasaseremrealizado = models.ManyToManyField(
        to=DiasDaSemana,
        null=False,
        blank=False,
        related_name='Rdiasdasemanaconfiguracoeslimpezapreidal'
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
        servicos_escalados_nomes= ", ".join(servico.nome for servico in self.ServicosEscalados.all())
        return f'{self.Areas} | {servicos_escalados_nomes}'


class ServicoLimpezaPredialAgendado(models.Model):
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

    DescricaoDoServico = models.TextField(
        max_length = 200,
        blank=False,
        null=False,
    )

    Areas = models.ForeignKey(
        to=AreaLimpezaPredial,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='Rarealimpezapredialagendado',
    )

    ServicosEscalados = models.ManyToManyField(
        to=CatalogodeServicoLimpezaPredial,
        blank=False,
        null=False,
        related_name='RServicosEscaladosLimpezaPredialServicoAgendado'
    )

    DataDeInicio = models.DateTimeField(
        null=True,
        blank=True
    )

    DataDeConclusao = models.DateTimeField(
        blank=True,
        null=True
    )

    DescricaoDoServico = models.TextField(
        max_length = 200,
        blank=False,
        null=False,
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

    def __str__(self):
        servicos_escalados_nomes = ", ".join(servico.nome for servico in self.ServicosEscalados.all())
        return f'{self.Areas} | {servicos_escalados_nomes} | {self.DataDeInicio.strftime("%d/%m/%Y %H:%M")}'



class FatoServicoLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Servico = models.ForeignKey(
        to=ServicoLimpezaPredialAgendado,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="RServicoServicoLimpezaPredialAgendado"
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
        related_name='RColaboradorFatoServicoLimpezaPredial'
    )

    foto_entrega = models.ImageField(
        upload_to="entrega_servico_limpeza_predial/%Y/%m/%d/",
        blank=True,
        null=True,
        max_length=2000,
    )

    def save(self, *args, **kwargs):
        if self.foto_entrega:
            self.foto_entrega = resize_image(self.foto_entrega, max_width=500)

        super(FatoServicoLimpezaPredial, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.Servico} | {self.data_hora_chegada_na_area} | {self.Gerente}'