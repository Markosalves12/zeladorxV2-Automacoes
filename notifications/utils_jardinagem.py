from notifications.utils import enviar_notificacao
from utils.utils import DataTableAndForms
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms

def send_notification_jardinagem(request, userid, email, username, dados, colunas, assunto, cabecalho, rodape):
    dt_and_forms = DataTableAndForms(
        request=request,
        model=dados,
        modelforms=ServicoJaridinagemAgendadoForms,
        per_page=20,
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        history_rout='checklists_jardinagem',
        userid=userid,
        id_random=False,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'ColaboradoresEscalados': 'ColaboradoresEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        }
    )

    forms, dados_paginados, get_data = dt_and_forms.get_data_and_forms()

    enviar_notificacao(
        destinatario=[email],
        assunto=assunto,
        contexto={
            'username': username,
            'email': email,
            'colunas': colunas,
            'dados_paginados': dados_paginados,
            'cabecalho': cabecalho,
            'rodape': rodape,
            'n_dados': len(dados),
        },
        template='notifications/notification_services.html'
    )


colunas_jardinagem = [
    {'nome': 'id', 'label': '#', 'largura': '10px'},
    {'nome': 'Areas', 'label': 'Área atendidada'},
    {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
    {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
    {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
    {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
    {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
    {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
    {'nome': 'novo_status', 'label': 'Status'},
]

colunas_retorno_proximo = [
    {'nome': 'id', 'label': '#', 'largura': '10px'},
    {'nome': 'Areas', 'label': 'Área atendidada'},
    {'nome': 'Periodicidade', 'label': 'Periodicidade'},
    {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
    {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
    {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
    {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
    {'nome': 'data_retorno_formatada', 'label': 'Data de retorno prevista'},
    {'nome': 'dias_restantes', 'label': 'Dias restantes'},
]
