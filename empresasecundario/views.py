from django.shortcuts import render, redirect
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.forms import EmpresaSecundariaForms
from utils.views import generic_view, edit_generic_view
from empresasecundario.utils import define_empresas

# Create your views here.
def empresas(request, userid):
    colunas = [
        {'nome': 'id', 'label': '#', 'largura': '10px'},
        {'nome': 'nome', 'label': 'Nome'},
        {'nome': 'razao_social', 'label': 'Razão social'},
        {'nome': 'CNPJ', 'label': 'CNPJ'},
        {'nome': 'setor', 'label': 'Setor'},
        {'nome': 'acoes', 'label': 'Ações'},
    ]

    empresas = define_empresas(request=request, userid=userid)
    empresas_primarias_ids = empresas['empresas_primarias_ids']

    return generic_view(
        request=request,
        model=EmpresaSecundaria.objects.filter(
            empresaprimaria__id_random__in=empresas_primarias_ids
        ),
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/DataTableAndForms.html',
        columns=colunas,
        edition_rout='editar_empresa',
        app_name='Empresas',
        text_button_open_modal='Adicionar nova empresa',
        text_button_save='Salvar empresa',
        header_model='Nova empresa',
        redirect_url='empresas',
        userid=userid
    )


def editar_empresa(request, userid, id_random):
    return edit_generic_view(
        request=request,
        model_class=EmpresaSecundaria,
        form_class=EmpresaSecundariaForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name='Editar empresa',
        redirect_url_name='editar_empresa',
        redirect_close_button='empresas',
    )