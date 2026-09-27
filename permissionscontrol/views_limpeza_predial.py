from django.shortcuts import reverse, redirect
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import (PermissionsAccessLimpezaPredial, PermissionsAccessJardinagem,
                                       PermissionsAccessEspecials)
from permissionscontrol.forms_limpeza_predial import PermissionsAccessLimpezaPredialForms
from gerente.models import Gerente
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions


# Create your views here.
def permissoes_limpeza_predial(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de permissão', 'link': ''},
        {'nome': 'Especiais', 'link': reverse('permissions_especials', kwargs={'userid': userid})},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('permissoes_jardinagem', kwargs={'userid': userid})})

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('permissoes_limpeza_predial', kwargs={'userid': userid})})
    else:
        return redirect('permissoes_jardinagem', userid)

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['301: Pode visualizar permissões de limpeza predial']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['300: Pode editar permissões de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Gerente', 'label': 'Nome'},
        {'nome': 'Permissions', 'label': 'Permissões'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=PermissionsAccessLimpezaPredial.objects.filter(
            Gerente__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Gerente__empresasecundaria__id_random__in=empresas_secundarias_ids,
            Gerente__empresasecundaria__setor__setor='Limpeza predial',
            Gerente__status='Mobilizado'
        ).distinct(),
        form_class=PermissionsAccessLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_permissoes_limpeza_predial',
        app_name='Permissões limpeza predial',
        form_search=PermissionsAccessLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Gerente': 'Gerente__id',
            'Permissions': 'Permissions'
        },
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar permissões',
        header_model='Novo gestor',
        redirect_url=reverse('permissoes_limpeza_predial', kwargs={'userid': userid}),
        link_tipos=tipos,
        userid=userid,
        permission_view=permission_view,
        permission_edit=permission_edit
    )


# o envio do id random esta quebrando o codigo
# definir o id random dentro da função
def editar_permissoes_limpeza_predial(request, userid, id_random):
    permissions_instance_especials = PermissionsAccessEspecials.objects.filter(
        Gerente__id_random=userid
    ).first()

    permissions_instance_jardinagem = PermissionsAccessJardinagem.objects.filter(
        Gerente__id_random=userid
    ).first()

    permissions_instance_limpeza_predial = PermissionsAccessLimpezaPredial.objects.filter(
        Gerente__id_random=userid
    ).first()

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de permissão', 'link': ''},
        {
            'nome': 'Especiais',
            'link': reverse('editar_permissoes_especials',
                            kwargs={'userid': userid, 'id_random': permissions_instance_especials.id_random})
        },
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(
            1,
            {
                'nome': 'Jardinagem',
                'link': reverse(
                    'editar_permissoes_jardinagem',
                    kwargs={
                        'userid': userid,
                        'id_random': permissions_instance_jardinagem.id_random
                    }
                )
            },
        )

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(
            2,
            {
                'nome': 'Limpeza predial',
                'link': reverse(
                    'editar_permissoes_limpeza_predial',
                    kwargs={
                        'userid': userid,
                        'id_random': permissions_instance_limpeza_predial.id_random
                    }
                )
            }
        )
    else:
        return redirect('permissoes_jardinagem', userid)

    gerente = PermissionsAccessLimpezaPredial.objects.get(
        id_random=id_random
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['300: Pode editar permissões de limpeza predial']
    )

    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessLimpezaPredial,
        form_class=PermissionsAccessLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name=f'Editar permissões limpeza predial',
        redirect_url_name=reverse('editar_permissoes_limpeza_predial', kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('permissoes_limpeza_predial', kwargs={'userid': userid}),
        link_tipos=None,
        permission_edit=permission_edit,
        url_desmobilize=None,
        url_rehabilitate=None,
        userid=userid,
    )
