from django.shortcuts import reverse, redirect
from areas.models_jardinagem import AreasJardins
from areas.forms_jardinagem import AreasJardinsForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, GenericIfDeleteView, GenericDeleteView
from localidade.models_Jardinagem import LocalidadeJardiangem
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas

# Create your views here.
def areas_jardins(request, userid):
    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de área', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem', 'link': reverse('areas_jardins', kwargs={'userid': userid})})
    else:
        return redirect('areas_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2,
                     {'nome': 'Limpeza predial', 'link': reverse('areas_limpeza_predial', kwargs={'userid': userid})})

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['252: Pode visualizar áreas de jardinagem']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['251: Pode editar áreas de jardinagem']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['250: Pode criar novas áreas de jardinagem']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'dimensao', 'label': 'Dimensão M²'},
        {'nome': 'Terreno', 'label': 'Terreno'},
        {'nome': 'vegetacao', 'label': 'vegetação'},
        {'nome': 'servico', 'label': 'Serviços'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=AreasJardins.objects.filter(
            localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ).distinct(),
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_jardins',
        history_rout='historico_de_servicos_areas_jardinagem',
        app_name='Áreas Jardinagem',
        form_search=AreasJardinsForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Terreno': 'Terreno__id',
            'vegetacao': 'vegetacao__id',
            'servico': 'servico__id',
            'localidade': 'localidade__id'
        },
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url=reverse('areas_jardins', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
    )


def editar_area_jardins(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['251: Pode editar áreas de jardinagem']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['254: Pode desmobilizar áreas de jardinagem']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['255: Pode reabilitar áreas de jardinagem']
    )

    return edit_generic_view(
        request=request,
        model_class=AreasJardins,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar área Jardins',
        redirect_url_name=reverse('editar_area_jardins', kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('areas_jardins', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_areas_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_areas_jardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteAreasJardinagem',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def areas_associadas_localidades_jardinagem(request, userid, id_random):
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
    else:
        return redirect('areas_limpeza_predial', userid)

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

    localidade = LocalidadeJardiangem.objects.get(
        id_random=id_random
    )

    objects = AreasJardins.objects.filter(
        localidade__id_random=id_random
    )

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['252: Pode visualizar áreas de jardinagem']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['251: Pode editar áreas de jardinagem']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['250: Pode criar novas áreas de jardinagem']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'Terreno', 'label': 'Terreno'},
        {'nome': 'vegetacao', 'label': 'vegetação'},
        {'nome': 'servico', 'label': 'Serviços'},
        {'nome': 'localidade', 'label': 'Localidade'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=objects,
        form_class=AreasJardinsForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_area_jardins',
        history_rout='historico_de_servicos_areas_jardinagem',
        app_name=f'Áreas Jardinagem - {localidade.nome}',
        form_search=AreasJardinsForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Terreno': 'Terreno__id',
            'vegetacao': 'vegetacao__id',
            'servico': 'servico__id',
            'localidade': 'localidade__id'
        },
        text_button_open_modal='Adicionar nova área',
        text_button_save='Salvar área',
        header_model='Nova área',
        redirect_url=reverse(areas_associadas_localidades_jardinagem, kwargs={'userid': userid, 'id_random': id_random}),
        link_tipos=tipos,
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
    )


def alterar_status_areas_jardinagem(request, userid, id_random, new_status):
    objeto = AreasJardins.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=AreasJardins,
        redirect_url_name=reverse('editar_area_jardins', kwargs={'userid': userid, 'id_random': id_random}),
        id_random=id_random,
        new_status=new_status,
        userid=userid,
        message=f'{objeto.nome} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto.nome} desmobilizado com sucesso'
    )



def IfDeleteAreasJardinagem(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericIfDeleteView(
        request,
        model=AreasJardins,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar área de jardinagem",
        url_delete=reverse(
            'DeleteAreasJardinagem',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('areas_jardins', kwargs={'userid': request.user.id_random})
    )




def DeleteAreasJardinagem(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas["empresas_primarias_ids"]
    empresas_secundarias_ids = empresas["empresas_secundarias_ids"]

    return GenericDeleteView(
        request,
        model=AreasJardins,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['253: Pode excluir áreas de jardinagem'],
        access_filters={
            "localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('areas_jardins', kwargs={'userid': request.user.id_random}),
    )