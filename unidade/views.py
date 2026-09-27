from django.shortcuts import reverse
from unidade.models import Unidade
from unidade.forms import UnidadeForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, GenericIfDeleteView, GenericDeleteView
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def unidades(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['342: Pode visualizar unidades']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['341: Pode editar unidades']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['340: Pode criar novas unidades']
    )

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']
    setores = empresas['setores']

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'empresasecundaria', 'label': 'Empresa'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Mapa'},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        colunas.insert(2, {'nome': 'linkmapajardinagem', 'label': 'Mapa Jardinagem'})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        colunas.insert(3, {'nome': 'linkmapalimnpezapredial', 'label': 'Mapa Limpeza Predial'})

    return generic_view(
        request=request,
        model=Unidade.objects.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria__id_random__in=empresas_secundarias_ids,
            id_random__in=unidades_secundarias_ids
        ).distinct(),
        form_class=UnidadeForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_unidade',
        history_rout='visualizar_unidade_jardinagem',
        app_name='Unidades',
        form_search=UnidadeForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'nome': 'nome__icontains',
            'empresasecundaria': 'empresasecundaria__id'
        },
        text_button_open_modal='Adicionar nova unidade',
        text_button_save='Salvar unidade',
        header_model='Nova unidade',
        redirect_url=reverse('unidades', kwargs={'userid': userid}),
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
    )


def editar_unidade(request, userid, id_random):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['341: Pode editar unidades']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['343: Pode excluir unidades']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['344: Pode desmobilizar unidades']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['345: Pode reabilitar unidades']
    )

    return edit_generic_view(
        request=request,
        model_class=Unidade,
        form_class=UnidadeForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar unidade',
        redirect_close_button=reverse('unidades', kwargs={'userid': userid}),
        redirect_url_name=reverse('editar_unidade', kwargs={'userid': userid, 'id_random': id_random}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_unidade',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_unidade',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteUnidade',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def alterar_status_unidade(request, userid, id_random, new_status):
    objeto = Unidade.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=Unidade,
        redirect_url_name=reverse(
            'editar_unidade',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        id_random=id_random,
        new_status=new_status,
        userid=userid,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )




def IfDeleteUnidade(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=Unidade,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['343: Pode excluir unidades'],
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar unidade",
        url_delete=reverse(
            'DeleteUnidade',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('unidades', kwargs={'userid': request.user.id_random})
    )



def DeleteUnidade(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    unidades_secundarias_ids = empresas['unidades_secundarias_ids']

    return GenericDeleteView(
        request,
        model=Unidade,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['343: Pode excluir unidades'],
        access_filters={
            "empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "empresasecundaria__id_random__in": empresas_secundarias_ids,
            "id_random__in": unidades_secundarias_ids
        },
        redirect_close_button=reverse('unidades', kwargs={'userid': request.user.id_random}),
    )