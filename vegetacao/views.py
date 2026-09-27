from django.shortcuts import reverse
from vegetacao.models import CatalogoVegetacao
from vegetacao.forms import CatalogoVegetacaoForm
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, GenericIfDeleteView, GenericDeleteView
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from areas.models_jardinagem import AreasJardins
from areas.forms_jardinagem import AreasJardinsForms


# Create your views here.
def vegetacao(request, userid):
    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['352: Pode visualizar vegetações']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['351: Pode editar vegetações']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['350: Pode criar novas vegetações']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'EmpresaSecundaria', 'label': 'Empresa'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Áreas associadas'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return generic_view(
        request=request,
        model=CatalogoVegetacao.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
        ).distinct(),
        form_class=CatalogoVegetacaoForm,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_vegetacao',
        history_rout='areas_associadas_vegetacao',
        app_name='vegetação',
        form_search=CatalogoVegetacaoForm(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'nome': 'nome',
            'EmpresaSecundaria': 'EmpresaSecundaria__id'
        },
        text_button_open_modal='Adicionar nova vegetação',
        text_button_save='Salvar vegetação',
        header_model='Nova vegetação',
        redirect_url=reverse('vegetacao', kwargs={'userid': userid}),
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_vegetacao(request, userid, id_random):
    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['351: Pode editar vegetações']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['353: Pode excluir vegetações']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['354: Pode desmobilizar vegetações']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['355: Pode reabilitar vegetações']
    )

    return edit_generic_view(
        request=request,
        model_class=CatalogoVegetacao,
        form_class=CatalogoVegetacaoForm,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar vegetação',
        redirect_close_button=reverse('vegetacao', kwargs={'userid': userid}),
        redirect_url_name=reverse('editar_vegetacao', kwargs={'userid': userid, 'id_random': id_random}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_vegetacao',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_vegetacao',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteCatalogoVegetacao',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def alterar_status_vegetacao(request, userid, id_random, new_status):
    objeto = CatalogoVegetacao.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=CatalogoVegetacao,
        redirect_url_name=reverse(
            'editar_vegetacao',
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


def areas_associadas_vegetacao(request, userid, id_random):
    vegetacao = CatalogoVegetacao.objects.get(
        id_random=id_random
    )

    objects = AreasJardins.objects.filter(
        vegetacao__id_random=id_random
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
        app_name=f'Áreas Jardinagem - {vegetacao.nome}',
        form_search=CatalogoVegetacaoForm(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'nome': 'nome',
            'EmpresaSecundaria': 'EmpresaSecundaria__id'
        },
        text_button_open_modal='Adicionar nova vegetação',
        text_button_save='Salvar área',
        header_model='Nova vegetação',
        redirect_url='vegetacao',
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid,
    )




def IfDeleteCatalogoVegetacao(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=CatalogoVegetacao,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['353: Pode excluir vegetações'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar vegetação",
        url_delete=reverse(
            'DeleteCatalogoVegetacao',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('vegetacao', kwargs={'userid': request.user.id_random})
    )



def DeleteCatalogoVegetacao(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDeleteView(
        request,
        model=CatalogoVegetacao,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['353: Pode excluir vegetações'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        redirect_close_button=reverse('vegetacao', kwargs={'userid': request.user.id_random}),
    )