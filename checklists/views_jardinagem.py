from django.shortcuts import reverse, redirect, render
from utils.views import (generic_view, edit_generic_view, generic_view_detailing_checklist, GenericIfDeleteView,
                         GenericDeleteView)
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from checklists.models import CheckListJardinagem
from checklists.forms_jardinagem import CheckListJardinagemForms
from servicos.models_jardinagem import ServicoJardinagemAgendado


# Create your views here.

"""('400: Pode criar novos checklists', '400: Pode criar novos checklists'),
('401: Pode editar checklists', '401: Pode editar checklists'),
('402: Pode visualizar checklists', '402: Pode visualizar checklists'),
('403: Pode excluir checklists', '403: Pode excluir checklists'),"""

def checklists_jardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['402: Pode visualizar checklists']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['401: Pode editar checklists']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['400: Pode criar novos checklists']
    )

    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)

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
        model=CheckListJardinagem.objects.filter(
            servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            servico_agendado__status__in=['Agendado', 'Em andamento'],
            servico_agendado__id_random=id_random
        ).distinct(),
        form_class=CheckListJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_checklist_jardinagem',
        history_rout='historico_de_servicos_areas_jardinagem',
        app_name=f'Checklist - {objeto}',
        form_search=CheckListJardinagemForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'status': 'status',
        },
        text_button_open_modal='Adicionar novo check',
        text_button_save='Salvar check',
        header_model='Novo check',
        redirect_url=reverse('checklists_jardinagem', kwargs={'userid': userid, 'id_random': id_random}),
        link_tipos=None,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
        id_random=id_random,
    )


def editar_checklist_jardinagem(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['401: Pode editar checklists']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['403: Pode excluir checklists']
    )

    obejeto = CheckListJardinagem.objects.get(id_random=id_random)
    id_random_servio = obejeto.servico_agendado.id_random

    return edit_generic_view(
        request=request,
        model_class=CheckListJardinagem,
        form_class=CheckListJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar checklist',
        redirect_url_name=reverse(
            'editar_checklist_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        redirect_close_button=reverse(
            'checklists_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random_servio
            }
        ),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=False,
        permission_rehabilitate=False,
        url_desmobilize=None,
        url_rehabilitate=None,
        userid=userid,
        id_random_especial=id_random_servio,
        url_if_delete=reverse(
            'IfDeleteCheckListJardins',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def view_detailing_checklists_jardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    model = CheckListJardinagem.objects.filter(
        servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
        servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        servico_agendado__id_random=id_random
    ).distinct()

    objeto = ServicoJardinagemAgendado.objects.get(id_random=id_random)


    return generic_view_detailing_checklist(
        request=request,
        userid=userid,
        id_random=id_random,
        model_class=model,
        app_name=f'Checklists: {objeto}'
    )



def IfDeleteCheckListJardins(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    id_random_servico = CheckListJardinagem.objects.get(id_random=id_random).servico_agendado.id_random

    return GenericIfDeleteView(
        request,
        model=CheckListJardinagem,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['403: Pode excluir checklists'],
        access_filters={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar checklist",
        url_delete=reverse(
            'DeleteCheckListJardins',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('checklists_jardinagem', kwargs={'userid': request.user.id_random, 'id_random': id_random_servico})
    )




def DeleteCheckListJardins(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    id_random_servico = CheckListJardinagem.objects.get(id_random=id_random).servico_agendado.id_random

    return GenericDeleteView(
        request,
        model=CheckListJardinagem,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['403: Pode excluir checklists'],
        access_filters={
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "servico_agendado__Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('checklists_jardinagem', kwargs={'userid': request.user.id_random, 'id_random': id_random_servico}),
    )