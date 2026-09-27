from django.shortcuts import reverse, redirect
from utils.views import generic_view, edit_generic_view
from permissionscontrol.models import (PermissionsAccessJardinagem, PermissionsAccessLimpezaPredial,
                                       PermissionsAccessEspecials)
from permissionscontrol.forms_jardinagem import PermissionsAccessJardinagemForms
from gerente.models import Gerente
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def permissoes_jardinagem(request, userid):
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
    else:
        return redirect('permissoes_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('permissoes_limpeza_predial', kwargs={'userid': userid})})


    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['301: Pode visualizar permissões de jardinagem']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['300: Pode editar permissões de jardinagem']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Gerente', 'label': 'Nome'},
        {'nome': 'Permissions', 'label': 'Permissões'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]


    return generic_view(
        request=request,
        model=PermissionsAccessJardinagem.objects.filter(
            Gerente__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Gerente__empresasecundaria__id_random__in=empresas_secundarias_ids,
            Gerente__empresasecundaria__setor__setor='Jardinagem',
            Gerente__status='Mobilizado'
        ).distinct(),
        form_class=PermissionsAccessJardinagemForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_permissoes_jardinagem',
        app_name='Permissões jardinagem',
        form_search=PermissionsAccessJardinagemForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Gerente': 'Gerente__id',
            'Permissions': 'Permissions'
        },
        text_button_open_modal='Adicionar novo gestor',
        text_button_save='Salvar permissões',
        header_model='Novo gestor',
        redirect_url=reverse('permissoes_jardinagem', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        userid=userid
    )


def editar_permissoes_jardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    permissions_instance_especials = PermissionsAccessEspecials.objects.filter(
        Gerente__id_random=userid
    ).first()

    permissions_instance_jardinagem = PermissionsAccessJardinagem.objects.filter(
        Gerente__id_random=userid
    ).first()

    permissions_instance_limpeza_predial = PermissionsAccessLimpezaPredial.objects.filter(
        Gerente__id_random=userid
    ).first()

    gerente = PermissionsAccessJardinagem.objects.get(
        id_random=id_random
    )

    tipos = [
        {'nome': 'Editar permissões', 'link': ''},
        {
            'nome': 'Especiais',
            'link': reverse(
                'editar_permissoes_especials',
                kwargs={
                    'userid': userid,
                    'id_random': permissions_instance_especials.id_random
                }
            )
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
            }
        )
    else:
        return redirect('permissoes_limpeza_predial', userid)

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

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['300: Pode editar permissões de jardinagem']
    )

    return edit_generic_view(
        request=request,
        model_class=PermissionsAccessJardinagem,
        form_class=PermissionsAccessJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name=f'Editar permissões jardinagem',
        redirect_url_name=reverse('editar_permissoes_jardinagem', kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('permissoes_jardinagem', kwargs={'userid': userid}),
        link_tipos=None,
        permission_edit=permission_edit,
        url_desmobilize=None,
        url_rehabilitate=None,
        userid=userid,
    )
