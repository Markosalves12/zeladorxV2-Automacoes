from django.shortcuts import render, redirect, reverse
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado
from servicos.forms_limpeza_predial import (FatoServicoLimpezaPredialForms,
                                            ServicoLimpezaPredialAgendadoForms)
from utils.views import generic_view, edit_generic_view, GenericIfDeleteView, GenericDeleteView
from permissionscontrol.utils import validate_permissions, verify_login
from empresasecundario.utils import define_empresas
from django.contrib import messages
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial
from servicos.utils_limpeza_predial import query_servicos_limpeza_predial_agendados_anotados

def agendar_servico_limpeza_predial(request, type, userid):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Agendar serviços', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(
            1,
            {
                'nome': 'Jardinagem',
                'link': reverse(
                    'agendar_servico_jardinagem',
                    kwargs={'type': type, 'userid': userid})
            },
        )

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(
            2,
            {
                'nome': 'Limpeza predial',
                'link': reverse(
                    'agendar_servico_limpeza_predial',
                    kwargs={'type': type, 'userid': userid}
                )
            }
        )
    else:
        return redirect('agendar_servico_jardinagem', type, userid)

    forms = ServicoLimpezaPredialAgendadoForms(request=request, userid=userid)

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    if request.method == 'POST':
        form = ServicoLimpezaPredialAgendadoForms(request.POST, request.FILES, request=request, userid=userid)
        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'Serviço(s) '
                        f'{", ".join([str(servico) for servico in form.cleaned_data["ServicosEscalados"].all()])} '
                        f'em {form.cleaned_data["Areas"]} agendado.'
            )

            return redirect('agendar_servico_limpeza_predial', type, userid)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    redirect_close_button = None

    if type == 'calendario':
        redirect_close_button = reverse('calendario_limpeza_predial', kwargs={'userid': userid})
    elif type == 'kanban':
        redirect_close_button = reverse('kanban_limpeza_predial', kwargs={'userid': userid})
    elif type == 'mapas':
        redirect_close_button = reverse('mapas_limpeza_predial', kwargs={'userid': userid})

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Agendar serviço de limpeza predial',
            'redirect_close_button': redirect_close_button,
            'redirect_url_name': reverse('agendar_servico_limpeza_predial', kwargs={'type': type, 'userid': userid}),
            'text_button_save': 'Agendar Serviço',
            'link_tipos': tipos,
            'permission_crate': permission_crate,
        }
    )


def servicos_agendados_limpeza_predial(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Serviços agendados', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('servicos_agendados_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid})})
    else:
        return redirect('servicos_agendados_jardinagem', userid)

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['322: Pode visualizar serviços agendados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'novo_status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Checklist'},
    ]

    agendado = query_servicos_limpeza_predial_agendados_anotados(
        request,
        userid,
        status_list=['Agendado', 'Em andamento']
    )

    return generic_view(
        request=request,
        model=agendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name='serviços agendados limpeza predial',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'TipoServico': 'TipoServico',
            'ServicosEscalados': 'ServicosEscalados__id',
            'DataDeInicio': 'DataDeInicio',
            'DataDeConclusao': 'DataDeConclusao'
        },
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url=reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
        history_rout='checklists_limpeza_predial'
    )


def editar_servico_limpeza_predial_agendado(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços agendados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoLimpezaPredialAgendado,
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name=reverse('editar_servico_limpeza_predial_agendado', kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        url_rehabilitate=reverse(
            'cancelar_servico_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'type': 'calendario'
            }
        ),
        url_desmobilize=reverse(
            'cancelar_servico_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'type': 'calendario'
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteServicoAgendadoLimpezaPredial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def realizar_servico_limpeza_predial_agendado(request, type, userid, id_random):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    forms = FatoServicoLimpezaPredialForms(
        initial={
            'Servico': objeto
        },
        id_random=id_random,
        request=request,
        userid=userid
    )

    permission_accompany = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['324: Pode acompanhar serviços agendados']
    )

    if request.method == 'POST':
        form = FatoServicoLimpezaPredialForms(request.POST, request.FILES, id_random=id_random,
                                              request=request, userid=userid)
        print(form.errors)
        if form.is_valid():
            form.save()
            objeto.status = 'Em andamento'
            objeto.save()
            messages.success(
                request=request,
                message=f'serviço, {objeto}, realizado'
            )
            return redirect('realizar_servico_limpeza_predial_agendado', type, userid, id_random)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    redirect_close_button_map = {
        "calendario": reverse('calendario_limpeza_predial', kwargs={'userid': userid}),
        "kanban": reverse('kanban_limpeza_predial', kwargs={'userid': userid}),
        "gantt": reverse('gantt_limpeza_predial', kwargs={'userid': userid}),
    }
    redirect_close_button = redirect_close_button_map.get(type, None)

    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Realizar serviço',
            'redirect_url_name': reverse(
                'realizar_servico_limpeza_predial_agendado',
                kwargs={
                    'type': type, 'userid': userid, 'id_random': id_random
                }
            ),
            'id_random': id_random,
            'redirect_close_button': redirect_close_button,
            'text_button': 'Salvar',
            'permission_accompany': permission_accompany
        }
    )


def cancelar_servico_limpeza_predial(request, userid, id_random, type):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    objeto.status = 'Cancelado'
    objeto.save()

    messages.error(
        request=request,
        message=f'serviço {objeto} cancelado'
    )

    if type == 'calendario':
        return redirect('calendario_limpeza_predial', userid)

    elif type == 'kanban':
        return redirect('kanban_limpeza_predial', userid)

    elif type == 'gantt':
        return redirect('gantt_limpeza_predial', userid)


def concluir_servico_limpeza_predial(request, userid, id_random, type):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)
    objeto.status = 'Concluido'
    objeto.save()

    messages.success(
        request=request,
        message=f'serviço {objeto} concluido com sucesso'
    )

    if type == 'calendario':
        return redirect('calendario_limpeza_predial', userid)

    elif type == 'kanban':
        return redirect('kanban_limpeza_predial', userid)

    elif type == 'gantt':
        return redirect('gantt_limpeza_predial', userid)


def view_detailing_limpeza_predial(request, userid, id_random):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['390: Pode visualizar o detalhamento de serviços']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'colaboradores_chamados', 'label': 'Colaborador envolvido'},
        {'nome': 'data_hora_chegada', 'label': 'Data e hora de chagada'},
        {'nome': 'data_hora_retorno', 'label': 'Data e hora de retorno'},
        {'nome': 'tempo_na_area', 'label': 'Tempo na área'},
    ]

    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)

    return generic_view(
        request=request,
        model=colect_dados_fato_servico_limpeza_predial(
            request=request,
            userid=userid,
            DataDeInicio=None,
            DataDeConclusao=None,
            ServicosEscalados=None,
            ColaboradoresEscalados=None,
            TipoServico=None,
            Areas=None,
            status=['Concluido', 'Agendado', 'Em andamento']
        ).filter(
            Servico__id_random=id_random
        ),
        form_class=ServicoLimpezaPredialAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_limpeza_predial_agendado',
        app_name=f'Detalhamento de execução -- {objeto.DescricaoDoServico}',
        form_search=ServicoLimpezaPredialAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'ServicosEscalados': 'Servico__ServicosEscalados__id',
            'DataDeInicio': 'Servico__DataDeInicio',
            'DataDeConclusao': 'Servico__DataDeConclusao'
        },
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_agendados_limpeza_predial',
        link_tipos=None,
        permission_view=permission_view,
        userid=userid
    )


def IfDeleteServicoAgendadoLimpezaPredial(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=ServicoLimpezaPredialAgendado,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar serviço",
        url_delete=reverse(
            'DeleteServicoAgendadoLimpezaPredial',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('servicos_agendados_limpeza_predial', kwargs={'userid': request.user.id_random})
    )



def DeleteServicoAgendadoLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDeleteView(
        request,
        model=ServicoLimpezaPredialAgendado,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('servicos_agendados_limpeza_predial', kwargs={'userid': request.user.id_random}),
    )