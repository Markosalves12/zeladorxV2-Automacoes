from django.shortcuts import reverse, redirect
from utils.views import generic_view, edit_generic_view, generic_view_detailing_checklist, GenericIfDeleteView, GenericDeleteView
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from checklists.models import CheckListLimpezaPredial
from checklists.forms_limpeza_predial import CheckListLimpezaPredialForms
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado

# Create your views here.
def checklists_limpeza_predial(request, userid, id_random):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['402: Pode visualizar checklists']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['401: Pode editar checklists']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['400: Pode criar novos checklists']
    )

    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'servico_agendado', 'label': 'Serviço agendado'},
        {'nome': 'descricao', 'label': 'Descrição do checklist'},
        {'nome': 'status', 'label': 'Status'},
        {'nome': 'atualizado_em', 'label': 'Atualizado em'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=CheckListLimpezaPredial.objects.filter(
            servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            servico_agendado__status__in=['Agendado', 'Em andamento'],
            servico_agendado__id_random=id_random
        ).distinct(),
        form_class=CheckListLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_checklist_limpeza_predial',
        history_rout='historico_de_servicos_areas_limpeza_predial',
        app_name=f'Checklist - {objeto}',
        form_search=CheckListLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'status': 'status',
        },
        text_button_open_modal='Adicionar novo check',
        text_button_save='Salvar check',
        header_model='Novo check',
        redirect_url=reverse('checklists_limpeza_predial',  kwargs={'userid': userid, 'id_random': id_random}),
        link_tipos=None,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
        id_random=id_random,
    )


def editar_checklist_limpeza_predial(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['401: Pode editar checklists']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['403: Pode excluir checklists']
    )


    obejeto = CheckListLimpezaPredial.objects.get(id_random=id_random)
    id_random_servio = obejeto.servico_agendado.id_random

    return edit_generic_view(
        request=request,
        model_class=CheckListLimpezaPredial,
        form_class=CheckListLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar checklist',
        redirect_url_name=reverse(
            'editar_checklist_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        redirect_close_button=reverse(
            'checklists_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random_servio
            }
        ),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=False,
        permission_rehabilitate=False,
        url_desmobilize=reverse(
            'alterar_status_areas_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_areas_limpeza_predial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        id_random_especial=id_random_servio,
        url_if_delete=reverse(
            'IfDeleteCheckListLimpezaPredial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def view_detailing_checklists_limpeza_predial(request, userid, id_random):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    model = CheckListLimpezaPredial.objects.filter(
        servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        # servico_agendado__status__in=['Agendado', 'Em andamento',],
        servico_agendado__id_random=id_random
    ).distinct()

    objeto = ServicoLimpezaPredialAgendado.objects.get(id_random=id_random)


    return generic_view_detailing_checklist(
        request=request,
        userid=userid,
        id_random=id_random,
        model_class=model,
        app_name=f'Checklists: {objeto}'
    )



def IfDeleteCheckListLimpezaPredial(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    id_random_servico = CheckListLimpezaPredial.objects.get(id_random=id_random).servico_agendado.id_random

    return GenericIfDeleteView(
        request,
        model=CheckListLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['403: Pode excluir checklists'],
        access_filters={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar checklist",
        url_delete=reverse(
            'DeleteCheckLimpezaPredial',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('checklists_limpeza_predial', kwargs={'userid': request.user.id_random, 'id_random': id_random_servico})
    )




def DeleteCheckLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    id_random_servico = CheckListLimpezaPredial.objects.get(id_random=id_random).servico_agendado.id_random

    return GenericDeleteView(
        request,
        model=CheckListLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['403: Pode excluir checklists'],
        access_filters={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('checklists_limpeza_predial', kwargs={'userid': request.user.id_random, 'id_random': id_random_servico}),
    )