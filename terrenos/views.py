from django.shortcuts import reverse
from terrenos.models import Terreno
from terrenos.forms import TerrenoForms
from utils.views import generic_view, edit_generic_view, gerneric_alter_status, GenericIfDeleteView, GenericDeleteView
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas
from areas.models_jardinagem import AreasJardins
from areas.forms_jardinagem import AreasJardinsForms
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def terrenos(request, userid):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['332: Pode visualizar terrenos']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['331: Pode editar terrenos']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['330: Pode criar novos terrenos']
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
        model=Terreno.objects.filter(
            EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            EmpresaSecundaria__id_random__in=empresas_secundarias_ids
        ).distinct(),
        form_class=TerrenoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_terreno',
        history_rout='areas_associadas_terrenos',
        app_name='Terrenos',
        form_search=TerrenoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'nome': 'nome',
            'EmpresaSecundaria': 'EmpresaSecundaria__id'
        },
        text_button_open_modal='Adicionar novo terreno',
        text_button_save='Salvar terreno',
        header_model='Novo terreno',
        redirect_url=reverse('terrenos', kwargs={'userid': userid}),
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )


def editar_terreno(request, userid, id_random):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['331: Pode editar terrenos']
    )

    permission_exclude = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['333: Pode excluir terrenos']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['334: Pode desmobilizar terrenos']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['335: Pode reabilitar terrenos']
    )

    return edit_generic_view(
        request=request,
        model_class=Terreno,
        form_class=TerrenoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar terreno',
        redirect_close_button=reverse('terrenos', kwargs={'userid': userid}),
        redirect_url_name=reverse('editar_terreno', kwargs={'userid': userid, 'id_random': id_random}),
        permission_edit=permission_edit,
        permission_exclude=permission_exclude,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_terreno',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_terreno',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteTerreno',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def alterar_status_terreno(request, userid, id_random, new_status):
    objeto = Terreno.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=Terreno,
        redirect_url_name=reverse(
            'editar_terreno',
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

def areas_associadas_terrenos(request, userid, id_random):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    terreno = Terreno.objects.get(
        id_random=id_random
    )

    objects = AreasJardins.objects.filter(
        Terreno__id_random=id_random
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
        app_name=f'Áreas Jardinagem - {terreno.nome}',
        form_search=TerrenoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'nome': 'nome',
            'EmpresaSecundaria': 'EmpresaSecundaria__id'
        },
        text_button_open_modal='Adicionar novo terreno',
        text_button_save='Salvar área',
        header_model='Novo terreno',
        redirect_url='terrenos',
        permission_view=permission_view,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        userid=userid
    )




def IfDeleteTerreno(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=Terreno,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['333: Pode excluir terrenos'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar terreno",
        url_delete=reverse(
            'DeleteTerreno',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('terrenos', kwargs={'userid': request.user.id_random})
    )



def DeleteTerreno(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDeleteView(
        request,
        model=Terreno,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['333: Pode excluir terrenos'],
        access_filters={
            "EmpresaSecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "EmpresaSecundaria__id_random__in": empresas_secundarias_ids
        },
        redirect_close_button=reverse('terrenos', kwargs={'userid': request.user.id_random}),
    )