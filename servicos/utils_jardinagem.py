from utils.utils import filtrar_unicos
from servicos.models_jardinagem import FatoServicoJardinagem, ServicoJardinagemAgendado
from django.db.models import (ExpressionWrapper, F, CharField,
                              IntegerField, DurationField, DateTimeField, FloatField, Value,
                              Case, When
                              )
from empresasecundario.utils import define_empresas
from django.utils import timezone
from django.db.models.functions import ExtractDay, Cast
from django.contrib.postgres.aggregates import StringAgg

def colect_dados_fato_servico_jardinagem(request, userid, DataDeInicio, DataDeConclusao, ServicosEscalados,
                                         ColaboradoresEscalados, TipoServico, Areas, status=list):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    # Adicione os dados do relatório ao arquivo Excel
    filters = {
        'Servico__status__in': status,
        'Servico__ColaboradoresEscalados__empresasecundaria__setor__setor': 'Jardinagem',
    }

    if DataDeInicio and DataDeInicio != "None":
        filters['Servico__DataDeInicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['Servico__DataDeConclusao__lte'] = DataDeConclusao

    if TipoServico and TipoServico != "None":
        filters['Servico__TipoServico'] = TipoServico

    if Areas and Areas != "None":
        filters['Servico__Areas__id'] = Areas

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['Servico__ServicosEscalados__id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['Servico__ColaboradoresEscalados__id__in'] = ColaboradoresEscalados


    dados = FatoServicoJardinagem.objects.annotate(
        id_acompanhamento=ExpressionWrapper(
            F('id'),
            output_field=IntegerField()
        ),
        id_random_acompanhamento=ExpressionWrapper(
            F('id_random'),
            output_field=CharField()
        ),
        id_agendamento=ExpressionWrapper(
            F('Servico__id'),
            output_field=IntegerField()
        ),
        id_random_agendamento=ExpressionWrapper(
            F('Servico__id_random'),
            output_field=CharField()
        ),
        colaboradores_chamados_id=ExpressionWrapper(
            F('Gerente__id'),
            output_field=IntegerField()
        ),
        colaboradores_chamados_id_random=ExpressionWrapper(
            F('Gerente__id_random'),
            output_field=CharField()
        ),
        colaboradores_chamados=ExpressionWrapper(
            F('Gerente__username'),
            output_field=CharField()
        ),
        data_hora_chegada=ExpressionWrapper(
            F('data_hora_chegada_na_area'),
            output_field=DateTimeField()
        ),
        data_hora_retorno=ExpressionWrapper(
            F('data_hora_retorno_area'),
            output_field=DateTimeField()
        ),
        tempo_na_area=ExpressionWrapper(
            F('data_hora_retorno_area') - F('data_hora_chegada_na_area'),
            output_field=DurationField()
        )
    ).distinct().filter(
        Servico__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Servico__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids
    )
    dados = filtrar_unicos(dados, **filters)

    return dados


def colect_dados_agendamentos_jardinagem(request, userid, DataDeInicio, DataDeConclusao, ServicosEscalados,
                                         ColaboradoresEscalados, TipoServico, Areas, status=list):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    # Adicione os dados do relatório ao arquivo Excel
    filters = {
        'status_servico__in': status,
        'tipodeempresa': 'Jardinagem',
    }

    if DataDeInicio and DataDeInicio != "None":
        filters['data_de_inicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['data_de_conclusao__lte'] = DataDeConclusao

    if TipoServico and TipoServico != "None":
        filters['tipo_agendamento'] = TipoServico

    if Areas and Areas != "None":
        filters['area_atendida_id'] = Areas

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['ServicosEscalados__id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['ColaboradoresEscalados__id__in'] = ColaboradoresEscalados

    dados = ServicoJardinagemAgendado.objects.annotate(
        # tipo de empresa
        tipodeempresa=Value('Jardinagem', output_field=CharField()),
        empresaprestadora=StringAgg(Cast(F('ServicosEscalados__EmpresaSecundaria__nome'), CharField()), delimiter=', ', distinct=True),
        # id de agendamento --> id_random
        id_agendamento=ExpressionWrapper(
            F('id'),
            output_field=IntegerField()
        ),
        id_random_agendamento=ExpressionWrapper(
            F('id_random'),
            output_field=CharField()
        ),
        #id config --> id_configuracao
        id_config=ExpressionWrapper(
            F('id_configuracao'),
            output_field=CharField()
        ),
        # tipo de agendamento --> TipoServico
        tipo_agendamento=ExpressionWrapper(
            F('TipoServico'),
            output_field=CharField()
        ),
        # descricao do serviço --> DescricaoDoServico
        descricao_do_servico=ExpressionWrapper(
            F('DescricaoDoServico'),
            output_field=CharField()
        ),
        # colaboradores chamados --> ColaboradoresEscalados
        colaboradores_chamados=StringAgg(Cast(F('ColaboradoresEscalados__username'), CharField()), delimiter=', ', distinct=True),
        colaboradores_chamados_id=StringAgg(Cast(F('ColaboradoresEscalados__id'), CharField()), delimiter=', ', distinct=True),
        colaboradores_chamados_id_random=StringAgg(Cast(F('ColaboradoresEscalados__id_random'), CharField()), delimiter=', ', distinct=True),
        # serviços solicitados --> ServicosEscalados
        servicos_solicitados=StringAgg(Cast(F('ServicosEscalados__nome'), CharField()), delimiter=', ', distinct=True),
        servicos_solicitados_id=StringAgg(Cast(F('ServicosEscalados__id'), CharField()), delimiter=', ', distinct=True),
        servicos_solicitados_id_random=StringAgg(Cast(F('ServicosEscalados__id_random'), CharField()), delimiter=', ', distinct=True),
        # data/hora de inicio --> DataDeInicio
        data_de_inicio=ExpressionWrapper(
            F('DataDeInicio'),
            output_field=DateTimeField()
        ),
        # data/hora de conclusao --> DataDeConclusao
        data_de_conclusao=ExpressionWrapper(
            F('DataDeConclusao'),
            output_field=DateTimeField()
        ),
        # foto antes --> foto_solicitacao
        antes=ExpressionWrapper(
            F('foto_solicitacao'),
            output_field=CharField()
        ),
        # foto final --> foto_entrega
        depois=ExpressionWrapper(
            F('foto_entrega'),
            output_field=CharField()
        ),
        # status do serviços --> status
        status_servico=ExpressionWrapper(
            F('status'),
            output_field=CharField()
        ),
        # Dadaos da área a ser atentida --> Areas
        area_atendida=ExpressionWrapper(
            F('Areas__nome'),
            output_field=CharField()
        ),
        area_atendida_id=ExpressionWrapper(
            F('Areas__id'),
            output_field=IntegerField()
        ),
        id_random_area=ExpressionWrapper(
            F('Areas__id_random'),
            output_field=CharField()
        ),
        periodicidade_de_retorno=ExpressionWrapper(
            F('Areas__periodicidade'),
            output_field=CharField()
        ),
        area_total=ExpressionWrapper(
            F('Areas__dimensao'),
            output_field=CharField()
        ),
        tipo_vegetacao=ExpressionWrapper(
            F('Areas__vegetacao__nome'),
            output_field=CharField()
        ),
        tipo_terreno=ExpressionWrapper(
            F('Areas__Terreno__nome'),
            output_field=CharField()
        ),
        # dados da localidade da área
        localidade=ExpressionWrapper(
            F('Areas__localidade__nome'),
            output_field=CharField()
        ),
        # dados da localidade da área
        lat=ExpressionWrapper(
            F('Areas__localidade__lat_med'),
            output_field=FloatField()
        ),
        long=ExpressionWrapper(
            F('Areas__localidade__long_med'),
            output_field=FloatField()
        ),
        # dados da unidade
        unidade=ExpressionWrapper(
            F('Areas__localidade__unidade__nome'),
            output_field=CharField()
        )
    ).distinct().filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids
    )
    dados = filtrar_unicos(dados, **filters)

    return dados

def query_servicos_jardinagem_agendados_anotados(request, userid, status_list):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    """
    Função genérica para filtrar serviços agendados com anotações de status calculado

    Args:
        empresas_primarias_ids: Lista de IDs de empresas primárias
        empresas_secundarias_ids: Lista de IDs de empresas secundárias
        status_list: Lista de status para filtrar
        userid: Id de usuario na url
    Returns:
        QuerySet com os resultados filtrados e anotados
    """

    return ServicoJardinagemAgendado.objects.filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        status__in=status_list
    ).annotate(
        dias_diferenca=ExtractDay(F('DataDeInicio') - timezone.now()),
        novo_status=Case(
            When(status='Em andamento', then=Value('Em andamento')),
            When(dias_diferenca__lt=0, then=Value('Atrasado')),
            When(dias_diferenca__gte=0, dias_diferenca__lte=7, then=Value('Próximo')),
            When(dias_diferenca__gt=7, then=Value('Agendado')),
            default=Value('Desconhecido'),
            output_field=CharField()
        )
    ).distinct()