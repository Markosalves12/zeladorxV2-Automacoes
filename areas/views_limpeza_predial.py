from django.shortcuts import reverse, redirect
from areas.models_limpeza_predial import AreaLimpezaPredial
from areas.forms_limpeza_predial import AreasLimpezaPredialForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, GenericIfDeleteView, GenericDeleteView
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def areas_limpeza_predial(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de área', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('areas_jardins', kwargs={'userid': userid})}, )

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2,
                     {'nome': 'Limpeza predial', 'link': reverse('areas_limpeza_predial', kwargs={'userid': userid})})
    else:
        return redirect('areas_jardins', userid)

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['252: Pode visualizar áreas de limpeza predial']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['251: Pode editar áreas de limpeza predial']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['250: Pode criar novas áreas de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'dimensao', 'label': 'Dimensão M²'},
        {'nome': 'servico', 'label': 'Serviço'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=AreaLimpezaPredial.objects.filter(
            localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids
        ).distinct(),
        form_class=AreasLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_limpeza_predial',
        history_rout='historico_de_servicos_areas_limpeza_predial',
        app_name='Áreas Limpeza Predial',
        form_search=AreasLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'servico': 'servico__id',
            'localidade': 'localidade__id'
        },
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url=reverse('areas_limpeza_predial', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_area_limpeza_predial(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['251: Pode editar áreas de limpeza predial']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['253: Pode excluir áreas de limpeza predial']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['254: Pode desmobilizar áreas de limpeza predial']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='limpeza_predial',
        permission_to_access=['255: Pode reabilitar áreas de limpeza predial']
    )

    return edit_generic_view(
        request=request,
        model_class=AreaLimpezaPredial,
        form_class=AreasLimpezaPredialForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar área limpeza predial',
        redirect_url_name=reverse('editar_area_limpeza_predial',  kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('areas_limpeza_predial', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
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
        url_if_delete=reverse(
            'IfDeleteAreasLimpezaPredial',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def areas_associadas_localidades_limpeza_predial(request, userid, id_random):
    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de área', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {
            'nome': 'Jardinagem',
            'link': reverse(
                'areas_jardins',
                kwargs={
                    'userid': userid,
                }
            )
        })

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {
            'nome': 'Limpeza predial',
            'link': reverse(
                'areas_limpeza_predial',
                kwargs={
                    'userid': userid,
                }
            )
        })
    else:
        return redirect('areas_jardins', userid)

    localidade = LocalidadeLimpezaPredial.objects.get(
        id_random=id_random
    )

    objects = AreaLimpezaPredial.objects.filter(
        localidade__id_random=id_random
    )

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['252: Pode visualizar áreas de limpeza predial']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['251: Pode editar áreas de limpeza predial']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type="limpeza_predial",
        permission_to_access=['250: Pode criar novas áreas de limpeza predial']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'dimensao', 'label': 'Dimensão'},
        {'nome': 'servico', 'label': 'Serviço'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=objects,
        form_class=AreasLimpezaPredialForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_limpeza_predial',
        history_rout='historico_de_servicos_areas_limpeza_predial',
        app_name=f'Áreas limpeza predial - {localidade.nome}',
        form_search=AreasLimpezaPredialForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'servico': 'servico__id',
            'localidade': 'localidade__id'
        },
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url=reverse('areas_associadas_localidades_limpeza_predial', kwargs={'userid': userid, 'id_random': id_random}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def alterar_status_areas_limpeza_predial(request, userid, id_random, new_status):
    objeto = AreaLimpezaPredial.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=AreaLimpezaPredial,
        redirect_url_name=reverse('editar_area_limpeza_predial', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status,
        userid=userid,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )



def IfDeleteAreasLimpezaPredial(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=AreaLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['253: Pode excluir áreas de limpeza predial'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar área de limpeza predial",
        url_delete=reverse(
            'DeleteAreasLimpezaPredial',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('areas_limpeza_predial', kwargs={'userid': request.user.id_random})
    )




def DeleteAreasLimpezaPredial(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=AreaLimpezaPredial,
        id_random=id_random,
        permission_type='limpeza_predial',
        permission_to_access=['253: Pode excluir áreas de limpeza predial'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('areas_limpeza_predial', kwargs={'userid': request.user.id_random}),
    )