from django.shortcuts import render, redirect, reverse
from servicos.models_jardinagem import ServicoJardinagemConfigurado
from servicos.forms_configuracoes_jardinagem import ServicoJardinagemConfiguradoForms
from utils.views import (generic_view, edit_generic_view, gerneric_alter_status, generic_view_history,
                         GenericIfDeleteView, GenericDeleteView)
from permissionscontrol.utils import validate_permissions, verify_login
from empresasecundario.utils import define_empresas
from django.contrib import messages
from servicos.models_jardinagem import ServicoJardinagemAgendado
from django.db.models import Case, When, Value, IntegerField

def configurar_servico_jardinagem(request, userid):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Configurar serviços', 'link': ''}
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('configurar_servico_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('configurar_servico_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('configurar_servico_limpeza_predial', kwargs={'userid': userid})}, )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['370: Pode configurar novos serviços']
    )

    forms = ServicoJardinagemConfiguradoForms(request=request, userid=userid)

    if request.method == 'POST':
        form = ServicoJardinagemConfiguradoForms(request.POST, request.FILES, request=request, userid=userid)

        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'Serviço(s) '
                        f'{", ".join([str(servico) for servico in form.cleaned_data["ServicosEscalados"].all()])} '
                        f'em {form.cleaned_data["Areas"]}, configurado.'
            )

            return redirect('configurar_servico_jardinagem', userid)

        messages.error(
            request=request,
            message=f'Algo de errado'
        )

    return render(
        request=request,
        template_name='DataTableAndForms/CreateObject.html',
        context={
            'forms': forms,
            'app_name': 'Configurar serviço de jardinagem',
            'redirect_close_button': reverse('calendario_jardinagem', kwargs={'userid': userid}),
            'redirect_url_name': reverse('configurar_servico_jardinagem', kwargs={'userid': userid}),
            'text_button_save': 'Configurar Serviço',
            'link_tipos': tipos,
            'permission_crate': permission_crate,
        }
    )


def servicos_configurados_jardinagem(request, userid):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']
    setores = empresas['setores']

    tipos = [
        {'nome': 'Serviços Configurados', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('servicos_configurados_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('servicos_configurados_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2, {'nome': 'Limpeza predial',
                         'link': reverse('servicos_configurados_limpeza_predial', kwargs={'userid': userid})})

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['372: Pode visualizar serviços configurados']
    )

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    permission_crate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['370: Pode configurar novos serviços']
    )

    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'Areas', 'label': 'Área'},
        {'nome': 'ServicosEscalados', 'label': 'Serivos planejados'},
        {'nome': 'tempomedioplanejado', 'label': 'Tempo médio planejado'},
        {'nome': 'diasaseremrealizado', 'label': 'Dias a serem realizados'},
        {'nome': 'horario_1', 'label': 'Horario 1'},
        {'nome': 'horario_2', 'label': 'Horario 2'},
        {'nome': 'horario_3', 'label': 'Horario 3'},
        {'nome': 'horario_4', 'label': 'Horario 4'},
        {'nome': 'horario_5', 'label': 'Horario 5'},
        {'nome': 'horario_6', 'label': 'Horario 6'},
        {'nome': 'horario_7', 'label': 'Horario 7'},
        {'nome': 'status', 'label': 'status'},
        {'nome': 'acoes', 'label': 'Ações'},
        {'nome': 'historico', 'label': 'Histórico'},
    ]

    return generic_view(
        request=request,
        model=ServicoJardinagemConfigurado.objects.filter(
            Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
        ).distinct(),
        form_class=ServicoJardinagemConfiguradoForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_servico_jardinagem_configurado',
        history_rout='historico_de_servicos_configurados_jardinagem',
        app_name='serviços configurados jardinagem',
        form_search=ServicoJardinagemConfiguradoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'diasaseremrealizado': 'diasaseremrealizado'
        },
        text_button_open_modal='configurar novo serviço',
        text_button_save='configurar serviço',
        header_model='solicitar serviço',
        redirect_url=reverse('servicos_configurados_jardinagem', kwargs={'userid': userid}),
        link_tipos=tipos,
        userid=userid,
        permission_edit=permission_edit,
        permission_crate=permission_crate,
        permission_view=permission_view
    )


def editar_servico_jardinagem_configurado(request, userid, id_random):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['371: Pode editar serviços configurados']
    )

    permission_desmobilize = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['374: Pode desmobilizar serviços configurados']
    )

    permission_rehabilitate = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['375: Pode reabilitar serviços configurados']
    )

    return edit_generic_view(
        request=request,
        model_class=ServicoJardinagemConfigurado,
        form_class=ServicoJardinagemConfiguradoForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar serviço',
        redirect_url_name=reverse('editar_servico_jardinagem_configurado',
                                  kwargs={'userid': userid, 'id_random': id_random}),
        redirect_close_button=reverse('servicos_configurados_jardinagem', kwargs={'userid': userid}),
        permission_edit=permission_edit,
        permission_exclude=True,
        permission_desmobilize=permission_desmobilize,
        permission_rehabilitate=permission_rehabilitate,
        url_desmobilize=reverse(
            'alterar_status_servico_jardinagem_configurado',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Desmobilizado',
            }
        ),
        url_rehabilitate=reverse(
            'alterar_status_servico_jardinagem_configurado',
            kwargs={
                'userid': userid,
                'id_random': id_random,
                'new_status': 'Mobilizado',
            }
        ),
        userid=userid,
        url_if_delete=reverse(
            'IfDeleteServicoJardinagemConfigurado',
            kwargs={
                'userid': userid,
                'id_random': id_random,
            }
        ),
    )


def alterar_status_servico_jardinagem_configurado(request, userid, id_random, new_status):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    objeto = ServicoJardinagemConfigurado.objects.get(id_random=id_random)
    return gerneric_alter_status(
        request=request,
        model_class=ServicoJardinagemConfigurado,
        redirect_url_name=reverse(
            'editar_servico_jardinagem_configurado',
            kwargs={
                'userid': userid,
                'id_random': id_random
            }
        ),
        id_random=id_random,
        new_status=new_status,
        userid=userid,
        message=f'{objeto} reabilitado com sucesso' if new_status == 'Mobilizado' else f'{objeto} desmobilizado com sucesso'
    )


def historico_de_servicos_configurados_jardinagem(request, userid, id_random):
    if not request.user.is_authenticated:
        messages.error(request, "usuario nao logado")
        return redirect('login')

    permission_extract_pdf = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['311: Pode extrair relatórios PDF de jardinagem']
    )

    permission_extract_xlsx = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['310: Pode extrair relatórios XLSX de jardinagem']
    )

    objeto = ServicoJardinagemConfigurado.objects.get(
        id_random=id_random
    )

    objetos = ServicoJardinagemAgendado.objects.filter(
        id_configuracao=id_random,
        status__in=['Concluido']
    ).annotate(
        diasaseremrealizado=Case(
            When(DataDeInicio__week_day=1, then=Value(7)),
            When(DataDeInicio__week_day=2, then=Value(1)),
            When(DataDeInicio__week_day=3, then=Value(2)),
            When(DataDeInicio__week_day=4, then=Value(3)),
            When(DataDeInicio__week_day=5, then=Value(4)),
            When(DataDeInicio__week_day=6, then=Value(5)),
            When(DataDeInicio__week_day=7, then=Value(6)),
            default=Value(8),
            output_field=IntegerField()
        )
    )

    return generic_view_history(
        request=request,
        userid=userid,
        id_random=id_random,
        app_name=f'Histórico de serviços {objeto}',
        objeto=objeto,
        objetos=objetos,
        type_exibition='jardinagem_agendado',
        type_export='configuracao',
        form_search=ServicoJardinagemConfiguradoForms(request=request, userid=userid, type='search'),
        sform_search=True,
        filtro_mapeamento={
            'Areas': 'Areas__id',
            'diasaseremrealizado': 'diasaseremrealizado'
        },
        export_pdf='exportar_relatorio_de_serivos_na_area_jardinagem_pdf',
        export_pdf_with_checklist='exportar_relatorio_de_serivos_na_area_jardinagem_pdf_with_checklist',
        export_excel='exportar_relatorio_de_serivos_na_area_Jardinagem_excel',
        export_excel_with_checklist='exportar_relatorio_de_serivos_na_area_Jardinagem_excel_with_checklist',
        foto_objeto=None,
        Foto=False,
        redirect_close_button='servicos_configurados_jardinagem',
        permission_extract_pdf=permission_extract_pdf,
        permission_extract_xlsx=permission_extract_xlsx,
        url_detalhamento='view_detailing_jardinagem',
        url_checklist='view_detailing_jardinagem'
    )



def IfDeleteServicoJardinagemConfigurado(request, userid, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericIfDeleteView(
        request,
        model=ServicoJardinagemConfigurado,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['373: Pode excluir serviços configurados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        template_name="DataTableAndForms/IfDelete.html",
        app_name="Deletar serviços configurados",
        url_delete=reverse(
            'DeleteServicoJardinagemConfigurado',
            kwargs={
                'id_random': id_random,
            }
        ),
        redirect_close_button=reverse('servicos_configurados_jardinagem', kwargs={'userid': request.user.id_random})
    )



def DeleteServicoJardinagemConfigurado(request, id_random):
    empresas = define_empresas(request=request, userid=request.user.id_random)
    empresas_primarias_ids = empresas['empresas_primarias_ids']
    empresas_secundarias_ids = empresas['empresas_secundarias_ids']

    return GenericDeleteView(
        request,
        model=ServicoJardinagemConfigurado,
        id_random=id_random,
        permission_type='jardinagem',
        permission_to_access=['373: Pode excluir serviços configurados'],
        access_filters={
            "Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in": empresas_primarias_ids,
            "Areas__localidade__unidade__empresasecundaria__id_random__in": empresas_secundarias_ids,
        },
        redirect_close_button=reverse('servicos_configurados_jardinagem', kwargs={'userid': request.user.id_random}),
    )