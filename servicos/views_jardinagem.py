from utils.utils import filtrar_unicos
from django.shortcuts import render, redirect, reverse
from servicos.models_jardinagem import ServicoJardinagemAgendado
from servicos.forms_jardinagem import ServicoJaridinagemAgendadoForms, FatoServicoJardinagemForms
from utils.views import generic_view, edit_generic_view, GenericIfDeleteView, GenericDeleteView
from permissionscontrol.utils import validate_permissions, verify_login
from empresasecundario.utils import define_empresas
from django.contrib import messages
from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem
from gerente.models import Gerente
from servicos.utils_jardinagem import query_servicos_jardinagem_agendados_anotados

# Create your views here.
def agendar_servico_jardinagem(request, type, userid):
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
                    kwargs={'type': type, 'userid': userid}
                )
            },
        )
    else:
        return redirect('agendar_servico_jardinagem', type, userid)

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

    forms = ServicoJaridinagemAgendadoForms(request=request, userid=userid)

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    if request.method == 'POST':
        form = ServicoJaridinagemAgendadoForms(request.POST, request.FILES, request=request, userid=userid)
        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'Serviço(s) '
                        f'{", ".join([str(servico) for servico in form.cleaned_data["ServicosEscalados"].all()])} '
                        f'em {form.cleaned_data["Areas"]} agendado.'
            )

            return redirect('agendar_servico_jardinagem', type, userid)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    redirect_close_button = None

    if type == 'calendario':
        redirect_close_button = reverse('calendario_jardinagem', kwargs={'userid': userid})
    elif type == 'kanban':
        redirect_close_button = reverse('kanban_jardinagem', kwargs={'userid': userid})
    elif type == 'mapas':
        redirect_close_button = reverse('mapas_jardinagem', kwargs={'userid': userid})

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Agendar serviço de jardinagem',
            'redirect_close_button': redirect_close_button,
            'redirect_url_name': reverse('agendar_servico_jardinagem', kwargs={'type': type, 'userid': userid}),
            'text_button_save': 'Agendar Serviço',
            'link_tipos': tipos,
            'permission_crate': permission_crate,
        }
    )


def servicos_agendados_jardinagem(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Serviços agendados', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('servicos_agendados_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('servicos_agendados_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('servicos_agendados_limpeza_predial', kwargs={'userid': userid})})

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['322: Pode visualizar serviços agendados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['320: Pode agendar novos serviços']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área atendidada'},
        {'nome': 'DataDeInicio', 'label': 'Data de inicio'},
        {'nome': 'DataDeConclusao', 'label': 'Data de conclusão'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'ColaboradoresEscalados', 'label': 'Colaboradores escalados'},
        {'nome': 'TipoServico', 'label': 'Tipo de agendamento'},
        {'nome': 'DescricaoDoServico', 'label': 'Descrição'},
        {'nome': 'novo_status', 'label': 'Status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Checklist'},
    ]

    auto_acompleshed = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['361: Pode acompanhar serviços agendados para si próprio']
    )

    agendado = query_servicos_jardinagem_agendados_anotados(
        request,
        userid,
        status_list=['Agendado', 'Em andamento']
    )

    # Verificação de permissões
    gerente = Gerente.objects.get(id_random=userid)
    if auto_acompleshed and not gerente.is_superuser:
        agendado = filtrar_unicos(agendado, ColaboradoresEscalados__id_random__in=[userid, 'MuUe1D3pvT3v'])
    return generic_view(
        request=request,
        model=agendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name='serviços agendados jardinagem',
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
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url=reverse('servicos_agendados_jardinagem', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_crate=permission_crate,
        permission_view=permission_view,
        permission_edit=permission_edit,
        userid=userid,
        history_rout='checklists_jardinagem'
    )


def editar_servico_jardinagem_agendado(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['321: Pode editar serviços agendados']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['323: Pode excluir serviços agendados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoJardinagemAgendado,
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name=reverse('editar_servico_jardinagem_agendado', kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('servicos_agendados_jardinagem', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        url_rehabilitate=reverse(
            'cancelar_servico_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'type': 'calendario'
            }
        ),
        url_desmobilize=reverse(
            'cancelar_servico_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'type': 'calendario'
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteServicoAgendadoJardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def realizar_servico_jardinagem_agendado(request, type, userid, id_random):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)

    forms = FatoServicoJardinagemForms(
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
        permission_type='jardinagem',
        permission_to_access=['324: Pode acompanhar serviços agendados']
    )

    if request.method == 'POST':
        form = FatoServicoJardinagemForms(request.POST, request.FILES, id_random=id_random,
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
            return redirect('realizar_servico_jardinagem_agendado', type, userid, id_random)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    redirect_close_button_map = {
        "calendario": reverse('calendario_jardinagem', kwargs={'userid': userid}),
        "kanban": reverse('kanban_jardinagem', kwargs={'userid': userid}),
        "gantt": reverse('gantt_jardinagem', kwargs={'userid': userid}),
    }
    redirect_close_button = redirect_close_button_map.get(type, None)

    return render(
        request=request,
        template_name='DataTableAndForms/EditObject.html',
        context={
            'forms': forms,
            'app_name': 'Realizar serviço',
            'redirect_url_name': reverse(
                'realizar_servico_jardinagem_agendado',
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


def cancelar_servico_jardinagem(request, userid, id_random, type):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)
    objeto.status = 'Cancelado'
    objeto.save()

    messages.error(
        request=request,
        message=f'serviço {objeto} cancelado'
    )

    if type == 'calendario':
        return redirect('calendario_jardinagem', userid)

    elif type == 'kanban':
        return redirect('kanban_jardinagem', userid)

    elif type == 'gantt':
        return redirect('gantt_jardinagem', userid)


def concluir_servico_jardinagem(request, userid, id_random, type):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)
    objeto.status = 'Concluido'
    objeto.save()

    messages.success(
        request=request,
        message=f'serviço {objeto} concluido com sucesso'
    )

    if type == 'calendario':
        return redirect('calendario_jardinagem', userid)

    elif type == 'kanban':
        return redirect('kanban_jardinagem', userid)

    elif type == 'gantt':
        return redirect('gantt_jardinagem', userid)


def view_detailing_jardinagem(request, userid, id_random):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['390: Pode visualizar o detalhamento de serviços']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['391: Pode editar o acompanhamento de servicos']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'colaboradores_chamados', 'label': 'Colaborador envolvido'},
        {'nome': 'data_hora_chegada', 'label': 'Data e hora de chagada'},
        {'nome': 'data_hora_retorno', 'label': 'Data e hora de retorno'},
        {'nome': 'tempo_na_area', 'label': 'Tempo na área'},
    ]

    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)

    return generic_view(
        request=request,
        model=colect_dados_fato_servico_jardinagem(
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
        form_class=ServicoJaridinagemAgendadoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_agendado',
        app_name=f'Detalhamento de execução -- {objeto.DescricaoDoServico}',
        form_search=ServicoJaridinagemAgendadoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'ColaboradoresEscalados': 'Gerente__id',
            'DataDeInicio': 'Servico__DataDeInicio',
            'DataDeConclusao': 'Servico__DataDeConclusao'
        },
        text_button_open_modal='agendar novo serviço',
        text_button_save='agendar serviço',
        header_model='solicitar serviço',
        redirect_url='servicos_agendados_jardinagem',
        link_tipos=None,
        permission_view=permission_view,
        permission_edit=permission_edit,
        userid=userid
    )


def IfDeleteServicoAgendadoJardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=ServicoJardinagemAgendado,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar serviço",
        url_delete=reverse(
            'DeleteServicoAgendadoJardinagem',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('servicos_agendados_jardinagem', kwargs={'userid': request.user.id_random})
    )



def DeleteServicoAgendadoJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDeleteView(
        request,
        model=ServicoJardinagemAgendado,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['323: Pode excluir serviços agendados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('servicos_agendados_jardinagem', kwargs={'userid': request.user.id_random}),
    )