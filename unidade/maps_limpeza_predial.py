from django.shortcuts import render, reverse, redirect
from unidade.models import Unidade
from permissionscontrol.utils import validate_permissions
from empresasecundario.utils import define_empresas


# Create your views here.
def visualizar_unidade_limpeza_predial(request, userid, id_random):
    objeto = Unidade.objects.get(
        id_random=id_random
    )

    permission_view = validate_permissions(
        request=request,
        userid=userid,
        permission_type='especials',
        permission_to_access=['342: Pode visualizar unidades']
    )

    empresas = define_empresas(request=request, userid=userid)
    setores = empresas['setores']

    tipos = [
        {'nome': 'Tipo de mapa', 'link': ''},
    ]

    if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
        tipos.insert(
            1,
            {
                'nome': 'Jardinagem',
                'link': reverse(
                    'visualizar_unidade_jardinagem',
                    kwargs={
                        'userid': userid,
                        'id_random': id_random
                    }
                )
            }
        )

    if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
        tipos.insert(
            2,
            {
                'nome': 'Limpeza predial',
                'link': reverse(
                    'visualizar_unidade_limpeza_predial',
                    kwargs={
                        'userid': userid,
                        'id_random': id_random
                    }
                )
            }
        )
    else:
        return redirect('visualizar_unidade_jardinagem', userid, id_random)

    return render(
        request=request,
        template_name="VisualizationMaps/VisualizationMaps.html",
        context={
            'app_name': f'Unidade {objeto.nome} - Mapa limpeza predial',
            'linkmapa': objeto.linkmapalimnpezapredial if objeto.linkmapalimnpezapredial else None,
            'objeto': objeto,
            'link_tipos': tipos,
            'permission_view': permission_view
        }
    )
