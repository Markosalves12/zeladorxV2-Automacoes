from django.shortcuts import render, redirect, get_object_or_404
from utils.utils import DataTableAndForms, aplicar_filtros_dinamicos, define_filters
from django.urls import reverse
from settings.utils import define_setting
from permissionscontrol.utils import configurate_permissions, verify_login
from django.contrib import messages
from dashboards.data_visualization_jardinagem import data_visualization_jardinagem_graphs
from empresaprimaria.models import EmpresaPrimaria
from unidade.forms import UnidadeForms
from unidade.models import Unidade
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions
from utils.utils import paginate
from django.db import router
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.utils import NestedObjects
from django.utils.http import urlencode
from utils.templatetags.zx_quick_create import safe_return_url


def quick_create_redirect(request, objeto, default_url):
    """'Salvar e voltar': retorna ao formulário de origem com o novo registro."""
    return_to = safe_return_url(request, request.POST.get('zx_return', ''))
    if not return_to or objeto is None:
        return redirect(default_url)

    separator = '&' if '?' in return_to else '?'
    query = urlencode({
        'zx_created': objeto.pk,
        'zx_created_label': str(objeto)[:200],
        'zx_field': request.POST.get('zx_field', '')[:120],
    })
    return redirect(f'{return_to}{separator}{query}')


def generic_view(request, model, form_class, template_name, columns, edition_rout, app_name,
                 text_button_open_modal, text_button_save, header_model,
                 redirect_url, form_search, filtro_mapeamento, id_random=False, sform_search=False, userid=False,
                 button_export_tittle=False, button_export_link='exportar_relatorio_de_serivos_Jardinagem_excel',
                 button_export_link_with_checklists='exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist',
                 status=['Mobilizado'],
                 link_tipos=None, modal_button=True, configurate_gerente=False, history_rout=False,
                 permission_view=True, permission_edit=False, permission_crate=False,
                 permission_accompany=False, views_on_maps=False, views_on_maps_url=None):
    if not request.user.is_authenticated:
        return redirect('logout')

    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    dt_and_forms = DataTableAndForms(
        request=request,
        model=model,
        modelforms=form_class,
        per_page=15,
        columns=columns,
        edition_rout=edition_rout,
        history_rout=history_rout,
        userid=userid,
        id_random=id_random,
        filtro_mapeamento=filtro_mapeamento
    )

    if request.method == 'POST':
        if id_random:
            form = form_class(request.POST, request.FILES, request=request, userid=userid, id_random=id_random)
        else:
            form = form_class(request.POST, request.FILES, request=request, userid=userid)

        # Adicionando a validação para o caso de 'UnidadeForms'
        if issubclass(form_class, UnidadeForms):
            # Pega os parâmetros de usuário
            empresas = define_empresas(request=request, userid=userid)
            empresas_primarias_ids = empresas['empresas_primarias_ids']

            # Identifica a empresa primária do usuário
            empresa_associada = EmpresaPrimaria.objects.get(id_random=empresas_primarias_ids[0])

            # Verifica a quantidade de unidades criadas associadas a essa empresa primária
            n_unidades_criadas = Unidade.objects.filter(
                empresasecundaria__empresaprimaria=empresa_associada
            ).distinct().count()  # Ajustei o filtro para ser mais direto, sem 'distinct'

            # Valida se a quantidade de unidades criadas ultrapassou o limite
            if n_unidades_criadas >= empresa_associada.N_unidades:
                messages.error(
                    request=request,
                    message=f'{empresa_associada.nome} atingiu o número máximo de unidades permitidas ({empresa_associada.N_unidades}).'
                )
                return redirect(redirect_url)

        if form.is_valid():
            if configurate_gerente:
                email = form.cleaned_data['email']
                objeto = form.save()

                define_setting(
                    request=request,
                    model_class=model,
                    email=email
                )

                configurate_permissions(
                    request=request,
                    model_class=model,
                    email=email
                )

                messages.info(
                    request=request,
                    message=f'alterações salvas'
                )

                return quick_create_redirect(request, objeto, redirect_url)

            else:
                objeto = form.save()

                messages.info(
                    request=request,
                    message=f'alterações salvas'
                )

                return quick_create_redirect(request, objeto, redirect_url)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    forms, dados_paginados, get_data = dt_and_forms.get_data_and_forms()

    url_action = redirect_url

    return render(
        request=request,
        template_name=template_name,
        context={
            'dados_paginados': dados_paginados,
            'forms': forms,
            'app_name': f'{app_name.capitalize()}',
            'colunas': columns,
            'text_button_open_modal': f'{text_button_open_modal.lower()}',
            'text_button_save': f'{text_button_save.lower()}',
            'header_model': f'{header_model.lower()}',
            'url_action': url_action,
            'form_search': form_search,
            'sform_search': sform_search,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'button_export_tittle': button_export_tittle,
            'button_export_link': reverse(
                f'{button_export_link}',
                kwargs={
                    'userid': userid,
                    'status': ','.join(status),
                    **get_data
                }
            ),
            'button_export_link_with_checklists': reverse(
                f'{button_export_link_with_checklists}',
                kwargs={
                    'userid': userid,
                    'status': ','.join(status),
                    **get_data
                }
            ),
            'link_tipos': link_tipos,
            'modal_button': modal_button,
            'permission_view': permission_view,
            'permission_edit': permission_edit,
            'permission_crate': permission_crate,
            'permission_accompany': permission_accompany,
            'views_on_maps': views_on_maps,
            'views_on_maps_url': views_on_maps_url
        }
    )


def edit_generic_view(request, model_class, form_class, template_name, id_random, app_name, redirect_url_name,
                      url_desmobilize, url_rehabilitate, userid,
                      redirect_close_button, link_tipos=None, permission_edit=False, permission_exclude=False,
                      permission_desmobilize=False, permission_rehabilitate=False, id_random_especial=False,
                      url_if_delete=False,
                      ):
    if not request.user.is_authenticated:
        return redirect('logout')

    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objeto = get_object_or_404(model_class, id_random=id_random)

    if id_random_especial:
        forms = form_class(
            instance=objeto,
            request=request,
            userid=request.session.get('userid', ''),
            id_random=id_random_especial
        )
    else:
        forms = form_class(
            instance=objeto,
            request=request,
            userid=request.session.get('userid', ''),
        )

    if request.method == 'POST':
        if id_random_especial:
            form = form_class(
                request.POST,
                request.FILES,
                instance=objeto,
                request=request,
                userid=request.session.get('userid', ''),
                id_random=id_random_especial
            )

        else:
            form = form_class(
                request.POST,
                request.FILES,
                instance=objeto,
                request=request,
                userid=request.session.get('userid', '')
            )

        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'alterações salvas'
            )

            return redirect(redirect_url_name)

        messages.error(
            request=request,
            message=f'{objeto}, Algo de errado'
        )

    return render(
        request=request,
        template_name=template_name,
        context={
            'forms': forms,
            'app_name': app_name,
            'id_random': id_random,
            'text_button': 'Salvar',
            'redirect_url_name': redirect_url_name,
            'redirect_close_button': redirect_close_button,
            'permission_edit': permission_edit,
            'link_tipos': link_tipos,
            'permission_exclude': permission_exclude,
            'permission_desmobilize': permission_desmobilize,
            'permission_rehabilitate': permission_rehabilitate,
            'url_desmobilize': url_desmobilize,
            'url_rehabilitate': url_rehabilitate,
            'url_if_delete': url_if_delete,
            'objeto': objeto
        }
    )


def gerneric_alter_status(request, model_class, redirect_url_name, id_random, new_status, message, userid):
    block = verify_login(request=request, userid=userid)
    if not request.user.is_authenticated:
        return redirect('logout')

    if block == True:
        return redirect('logout')

    objeto = get_object_or_404(model_class, id_random=id_random)
    objeto.status = new_status
    objeto.save()

    if new_status == 'Mobilizado':
        messages.success(
            request=request,
            message=message
        )

    elif new_status == 'Desmobilizado':
        messages.warning(
            request=request,
            message=message
        )

    return redirect(redirect_url_name)


def generic_view_history(request, userid, id_random, app_name, objeto, objetos, type_exibition, type_export,
                         form_search,
                         sform_search, filtro_mapeamento, export_pdf, export_pdf_with_checklist,
                         export_excel, export_excel_with_checklist, redirect_close_button,
                         url_detalhamento, url_checklist,
                         foto_objeto=None, Foto=False, permission_extract_pdf=False, permission_extract_xlsx=False):
    if not request.user.is_authenticated:
        return redirect('logout')

    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    get_data = define_filters(request=request, isnull=True)

    if request.method == 'GET':
        get_data = request.GET.dict()
        objetos = aplicar_filtros_dinamicos(objetos, get_data, filtro_mapeamento)

        get_data = define_filters(request=request, isnull=False)

    dados_paginados = paginate(
        request=request,
        data_objects=objetos,
        per_page=2
    )

    return render(
        request=request,
        template_name='history/history.html',
        context={
            'app_name': f'{app_name}',
            'objeto': objeto,
            'foto_objeto': foto_objeto,
            'Foto': Foto,
            'type_exibition': type_exibition,
            'form_search': form_search,
            'sform_search': sform_search,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'dados_paginados': dados_paginados,
            'permission_extract_pdf': permission_extract_pdf,
            'export_pdf': reverse(
                f'{export_pdf}',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': f'{type_export}',
                }
            ),
            'export_pdf_with_checklist': reverse(
                f'{export_pdf_with_checklist}',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': f'{type_export}',
                }
            ),
            'permission_extract_xlsx': permission_extract_xlsx,
            'export_excel': reverse(
                viewname=f'{export_excel}',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': f'{type_export}',
                }
            ),
            'export_excel_with_checklist': reverse(
                viewname=f'{export_excel_with_checklist}',
                kwargs={
                    'userid': userid,
                    'id_random': id_random,
                    **get_data,
                    'type': f'{type_export}',
                }
            ),
            'redirect_close_button': reverse(redirect_close_button, kwargs={'userid': userid}),
            'url_detalhamento': url_detalhamento,
            'url_checklist': url_checklist
        }
    )


def generic_view_detailing_checklist(request, userid, id_random, model_class, app_name):
    dados_paginados = paginate(request, model_class, per_page=5)

    return render(
        request=request,
        template_name='checklists/checklists.html',
        context={
            'app_name': f'{app_name}',
            'dados_paginados': dados_paginados,
        }
    )


def generic_view_maps(request, model, form_class, template_name, app_name,
                      text_button_open_modal, text_button_save, header_model,
                      redirect_url, form_search, filtro_mapeamento, color,
                        redirect_close_button,
                      id_random=False, sform_search=False, userid=False,
                      link_tipos=None, modal_button=True,
                      permission_view=True, permission_crate=False):
    if not request.user.is_authenticated:
        return redirect('logout')

    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    dt_and_forms = DataTableAndForms(
        request=request,
        model=model,
        modelforms=form_class,
        per_page=15,
        columns=[
            {'nome': 'id', 'label': '#', 'largura': '10px'},
            {'nome': 'unidade_nome', 'label': 'Nome'},
            {'nome': 'lat_localidade', 'label': 'Lat. média'},
            {'nome': 'long_localidade', 'label': 'Long. média'},
            {'nome': 'area_total', 'label': 'Área'},
            {'nome': 'localidade_nome', 'label': 'Nome localidade'},
        ],
        edition_rout='editar_localidade_jardinagem',
        history_rout=False,
        userid=userid,
        id_random=id_random,
        filtro_mapeamento=filtro_mapeamento
    )

    if request.method == 'POST':
        if id_random:
            form = form_class(request.POST, request.FILES, request=request, userid=userid, id_random=id_random)
        else:
            form = form_class(request.POST, request.FILES, request=request, userid=userid)

        if form.is_valid():
            form.save()

            messages.info(
                request=request,
                message=f'alterações salvas'
            )

            return redirect(redirect_url)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    forms, dados_paginados, get_data = dt_and_forms.get_data_and_forms()

    url_action = redirect_url

    fig_mapa_localidades = data_visualization_jardinagem_graphs(request, userid, dados_paginados).create_fig_maps(
        name_fig='fig_mapa_localidades',
        color=color,
    )

    return render(
        request=request,
        template_name=template_name,
        context={
            'forms': forms,
            'app_name': f'{app_name.capitalize()}',
            'text_button_open_modal': f'{text_button_open_modal.lower()}',
            'text_button_save': f'{text_button_save.lower()}',
            'header_model': f'{header_model.lower()}',
            'url_action': url_action,
            'form_search': form_search,
            'sform_search': sform_search,
            'allowed_fields': list(filtro_mapeamento.keys()),
            'link_tipos': link_tipos,
            'modal_button': modal_button,
            'permission_view': permission_view,
            'permission_crate': permission_crate,
            'redirect_close_button': redirect_close_button,
            **fig_mapa_localidades,
        }
    )


def flatten_nested(obj_list, depth=0):
    """
    Converte estrutura aninhada do Django Admin (nested()) em lista formatada.
    """
    flat = []
    for item in obj_list:
        if isinstance(item, list):
            flat.extend(flatten_nested(item, depth + 1))
        else:
            flat.append(f"{'  ' * depth}- {str(item)}")
    return flat



def GenericIfDeleteView(
    request,
    *,
    model,
    id_random: str,
    permission_type: str,
    permission_to_access: list,
    access_filters: dict,
    template_name: str,
    app_name: str,
    url_delete: str,
    redirect_close_button: str,
):
    user_id_random = request.user.id_random

    # Validação de permissão
    permission_exclude = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    )

    # Busca com filtros de acesso (ex: organização, empresa)
    instance = model.objects.get(id_random=id_random, **access_filters)

    # Coleta de objetos relacionados que seriam deletados
    collector = NestedObjects(using=router.db_for_write(model))
    collector.collect([instance])
    nested_tree = collector.nested()
    deletions_list = flatten_nested(nested_tree)

    return render(
        request=request,
        template_name=template_name,
        context={
            "app_name": app_name,
            'permission_exclude': permission_exclude,
            "objeto_principal": str(instance),
            "resumo": {
                    model.__name__: len(objs)
                    for model, objs in collector.model_objs.items()
            },
            "objetos_em_cascata": deletions_list,
            "total_items":sum({
                    model.__name__: len(objs)
                    for model, objs in collector.model_objs.items()
            }.values()),
            "url_delete": url_delete,
            "redirect_close_button": redirect_close_button
        }
    )




def GenericDeleteView(
    request,
    *,
    model,
    id_random: str,
    permission_type: str,
    permission_to_access: list,
    access_filters: dict,
    redirect_close_button,
):
    user_id_random = request.user.id_random

    # 1. Validação de permissão
    has_permission = validate_permissions(
        request=request,
        userid=user_id_random,
        permission_type=permission_type,
        permission_to_access=permission_to_access
    )

    if not has_permission:
        return redirect(redirect_close_button)

    # 2. Busca com filtros de acesso (escopo de empresas, etc.)
    try:
        instance = model.objects.get(id_random=id_random, **access_filters)
    except model.DoesNotExist:
        return redirect()

    # 3. Deletar objeto (em cascata, conforme relações)
    instance_repr = str(instance)
    instance.delete()

    return redirect(redirect_close_button)