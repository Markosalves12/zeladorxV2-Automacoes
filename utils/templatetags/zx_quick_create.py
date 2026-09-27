"""
Criação rápida de registros a partir de listas (dropdowns) obrigatórias.

Uso no template, dentro do <form>:
    {% load zx_quick_create %}
    {% zx_quick_create forms %}

Para cada campo obrigatório de escolha única cujo model esteja em
QUICK_CREATE_ROUTES, o JS (dist/js/zeladorx-quick-create.js) adiciona o
botão "Novo". O usuário cria o registro na tela do cadastro relacionado e,
com "Salvar e voltar", retorna ao formulário original com o rascunho
restaurado e o novo item já selecionado.
"""
from django import forms as django_forms
from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.html import json_script
from django.utils.http import url_has_allowed_host_and_scheme

register = template.Library()

# nome do model -> (nome da rota da listagem com modal de criação, rótulo)
QUICK_CREATE_ROUTES = {
    'Unidade': ('unidades', 'unidade'),
    'Terreno': ('terrenos', 'terreno'),
    'CatalogoVegetacao': ('vegetacao', 'vegetação'),
    'LocalidadeJardiangem': ('localidades_jardinagem', 'localidade'),
    'LocalidadeLimpezaPredial': ('localidades_limpeza_predial', 'localidade'),
    'AreasJardins': ('areas_jardins', 'área'),
    'AreaLimpezaPredial': ('areas_limpeza_predial', 'área'),
    'CatalogodeServicoJardinagem': ('catalogo_de_servicos_jardinagem', 'serviço'),
    'CatalogodeServicoLimpezaPredial': ('catalogo_de_servicos_limpeza_predial', 'serviço'),
}


def safe_return_url(request, value):
    """Aceita apenas caminhos internos do próprio sistema."""
    if not value or not value.startswith('/') or value.startswith('//'):
        return ''
    if not url_has_allowed_host_and_scheme(value, allowed_hosts={request.get_host()}):
        return ''
    return value


def quick_create_fields(form, request):
    userid = request.session.get('userid', '')
    if not form or not userid:
        return {}

    fields = {}
    for name, field in form.fields.items():
        if not field.required or isinstance(field, django_forms.ModelMultipleChoiceField):
            continue
        if not isinstance(field, django_forms.ModelChoiceField):
            continue
        if not isinstance(field.widget, django_forms.Select):
            continue

        route = QUICK_CREATE_ROUTES.get(field.queryset.model.__name__)
        if not route:
            continue

        try:
            url = reverse(route[0], kwargs={'userid': userid})
        except NoReverseMatch:
            continue

        fields[form.add_prefix(name)] = {'url': url, 'label': route[1]}
    return fields


@register.simple_tag(takes_context=True)
def zx_quick_create(context, form=None):
    request = context.get('request')
    if request is None:
        return ''

    data = request.POST if request.method == 'POST' else request.GET
    config = {
        'fields': quick_create_fields(form, request),
        # Estado de quem está criando um registro para voltar a outro formulário
        'returnTo': safe_return_url(request, data.get('zx_return', '')),
        'returnField': data.get('zx_field', '')[:120],
    }
    return json_script(config, 'zx-quick-create-config')
