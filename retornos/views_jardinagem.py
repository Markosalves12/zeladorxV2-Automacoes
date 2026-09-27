from django.shortcuts import render, reverse, redirect
from empresasecundario.utils import define_empresas
from utils.views import generic_view
from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.db.models import F, Value, CharField, Case, When, IntegerField
from django.db.models import ExpressionWrapper, DurationField
from django.utils import timezone
from retornos.utils import formatar_tempo_desde, calcular_data_retorno_formatada
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms

# Create your views here.
def tempo_desde_ultimo_atendimento_jardinagem(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'Periodicidade', 'label': 'Periodicidade'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'tempo_desde_ultimo_atendimento', 'label': 'Tempo'},
        {'nome': 'data_retorno_formatada', 'label': 'Data de retorno prevista'},
        {'nome': 'dias_restantes', 'label': 'Dias restantes'},
    ]

    tipos = [
        {'nome': 'Retornos', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('tempo_desde_ultimo_atendimento_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('tempo_desde_ultimo_atendimento_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('tempo_desde_ultimo_atendimento_limpeza_predial', kwargs={'userid': userid})})

    # Dias desde o atendimento até agora
    dados = ServicoJardinagemAgendado.objects.filter(
        Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        Areas__status='Mobilizado',
        status='Concluido'
    ).distinct('Areas__id_random').order_by('Areas__id_random', '-DataDeConclusao').annotate(
        dias_diferenca=ExpressionWrapper(
            timezone.now() - F('DataDeConclusao'),
            output_field=DurationField()
        ),
        Periodicidade=ExpressionWrapper(
            F('Areas__periodicidade'),
            output_field=CharField()
        )
    )

    for obj in dados:
        obj.tempo_desde_ultimo_atendimento = formatar_tempo_desde(obj.dias_diferenca)
        obj.data_retorno_formatada, obj.dias_restantes = calcular_data_retorno_formatada(obj.DataDeConclusao.date(), obj.Periodicidade)


    return generic_view(
        request=request,
        link_tipos=tipos,
        model=dados,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_unidade',
        history_rout='visualizar_unidade_jardinagem',
        app_name='Tempo desde o ultimo atendimento (Áreas jardinagem)',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='Adicionar nova unidade',
        text_button_save='Salvar unidade',
        header_model='Nova unidade',
        redirect_url=reverse('unidades', kwargs={'userid': userid}),
        permission_view=True,
        permission_edit=True,
        permission_crate=False,
        userid=userid,
    )