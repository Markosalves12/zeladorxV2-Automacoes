from django.shortcuts import reverse, redirect
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.forms import EmpresaSecundariaForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, GenericIfDeleteView, GenericDeleteView
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions

# Create your views here.
def empresas_jardinagem(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de empresa', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('empresas_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('empresas_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial', 'link': reverse('empresas_limpeza_predial', kwargs={'userid': userid})})


    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['272: Pode visualizar empresas']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['271: Pode editar empresas']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['270: Pode criar novas empresas']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'setor', 'label': 'Setor'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    return generic_view(
        request=request,
        model=EmpresaSecundaria.objects.filter(
            empresaprimaria__id_random__in=empresas_primarias_ids,
            setor__setor__in=['Jardinagem']
        ).distinct(),
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_empresa_jardinagem',
        app_name='Empresas de jardinagem',
        form_search=EmpresaSecundariaForms(request=request, userid=userid, type='search'),
        sform_search=False,
        filtro_mapeamento={
            'servico': 'servico__id',
            'localidade': 'localidade__id'
        },
        text_button_open_modal='Adicionar nova empresa',
        text_button_save='Salvar empresa',
        header_model='Nova empresa',
        redirect_url=reverse('empresas_jardinagem', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_empresa_jardinagem(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['271: Pode editar empresas']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['273: Pode excluir empresas']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['274: Pode desmobilizar empresas']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['275: Pode reabilitar empresas']
    )

    return edit_generic_view(
        request=request,
        model_class=EmpresaSecundaria,
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar empresa',
        redirect_url_name=reverse('editar_empresa_jardinagem', kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('empresas_jardinagem', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_rehabilitate=permission_rehabilitate,
        permission_desmobilize=permission_desmobilize,
        url_desmobilize=reverse(
            'alterar_status_empresa_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_empresa_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteEmpresaSecundariaJardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def alterar_status_empresa_jardinagem(request, userid, id_random, new_status):
    objeto = EmpresaSecundaria.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=EmpresaSecundaria,
        redirect_url_name=reverse('editar_empresa_jardinagem', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status,
        userid=userid,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )



def IfDeleteEmpresaSecundariaJardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]

    return GenericIfDeleteView(
        request,
        model=EmpresaSecundaria,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['273: Pode excluir empresas'],
        access_filters={
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Jardinagem']
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar empresas",
        url_delete=reverse(
            'DeleteEmpresaSecundariaJardinagem',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('empresas_jardinagem', kwargs={'userid': request.user.id_random})
    )



def DeleteEmpresaSecundariaJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]

    return GenericDeleteView(
        request,
        model=EmpresaSecundaria,
        id_random=id_random,
        permission_type='especials',
        permission_to_access=['273: Pode excluir empresas'],
        access_filters={
            "empresaprimaria__id_random__in": empresas_primarias_ids,
            "setor__setor__in": ['Jardinagem']
        },
        redirect_close_button=reverse('empresas_jardinagem', kwargs={'userid': request.user.id_random}),
    )