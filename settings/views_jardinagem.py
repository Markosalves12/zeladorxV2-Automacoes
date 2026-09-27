from django.shortcuts import render, redirect, reverse
from settings.models import SettingServicosGerenteJardinagem
from settings.forms_jardinagem import SettingServicosGerenteJardinagemForms
from utils.views import edit_generic_view
from empresasecundario.utils import define_empresas
from permissionscontrol.utils import validate_permissions


def configurar_notificacoes_jardinagem(request, userid):
    objeto = SettingServicosGerenteJardinagem.objects.get(
        Gerente__id_random=userid
    )

    id_random = objeto.id_random

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de Configuração', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(1, {'nome': 'Jardinagem',
                         'link': reverse('configurar_notificacoes_jardinagem', kwargs={'userid': userid})})
    else:
        return redirect('configurar_notificacoes_limpeza_predial', userid)

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(2,
                     {'nome': 'Limpeza predial',
                      'link': reverse('configurar_notificacoes_limpeza_predial', kwargs={'userid': userid})})

    permission_edit = validate_permissions(
        request=request,
        userid=userid,
        permission_type='jardinagem',
        permission_to_access=['410: Pode editar o recebimento de notificações gerais']
    )

    return edit_generic_view(
        request=request,
        model_class=SettingServicosGerenteJardinagem,
        form_class=SettingServicosGerenteJardinagemForms,
        template_name='DataTableAndForms/EditObject.html',
        id_random=id_random,
        app_name=f'Configurar notificações de jardinagem',
        redirect_url_name=reverse('configurar_notificacoes_jardinagem', kwargs={'userid': userid}),
        redirect_close_button=reverse('calendario_jardinagem', kwargs={'userid': userid}),
        link_tipos=tipos,
        permission_edit=permission_edit,
        url_desmobilize=False,
        url_rehabilitate=False,
        userid=userid,
    )
