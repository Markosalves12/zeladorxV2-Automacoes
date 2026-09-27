from django.shortcuts import render
from notifications.utils_limpeza_predial import send_notification_limpeza_predial
from servicos.utils_limpeza_predial import query_servicos_limpeza_predial_agendados_anotados
from settings.models import SettingServicosGerenteLimpezaPredial
from empresasecundario.utils import define_empresas
from notifications.utils_limpeza_predial import colunas_limpeza_predial

def send_notification_servicos_atrasados_limpeza_predial(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteLimpezaPredial.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
            configuracoes = SettingServicosGerenteLimpezaPredial.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosAtrasados == True:
                atrasados = query_servicos_limpeza_predial_agendados_anotados(
                    request=request,
                    userid=Gerente.id_random,
                    status_list=['Agendado', 'Em andamento']
                ).filter(
                    novo_status='Atrasado'
                )

                cabecalho = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Serviço(s) atrasado(s), sua organização possui {len(atrasados)} serviço(s) em atraso, considere inicia-lo(s) ou cancela-los</br>
                </div>"""

                rodape = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Sua organização não possui serviço(s) em atraso</br>
                </div>"""

                send_notification_limpeza_predial(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=atrasados,
                    colunas=colunas_limpeza_predial,
                    assunto="Limpeza predial | Serviços atrasados",
                    cabecalho=cabecalho,
                    rodape=rodape
                )


    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )


def send_notification_servicos_proximos_limpeza_predial(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteLimpezaPredial.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
            configuracoes = SettingServicosGerenteLimpezaPredial.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosProximos == True:
                proximos = query_servicos_limpeza_predial_agendados_anotados(
                    request,
                    userid=Gerente.id_random,
                    status_list=['Agendado', 'Em andamento']
                ).filter(
                    novo_status='Proximo'
                )

                cabecalho = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Serviço(s) se aproximando, sua organização possui {len(proximos)} serviço(s) próximo, prepare-se para inicia-lo(s)</br>
                </div>"""

                rodape = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Sua organização não possui serviço(s) se aproximando</br>
                </div>"""

                send_notification_limpeza_predial(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=proximos,
                    colunas=colunas_limpeza_predial,
                    assunto="Limpeza predial | Serviços próximos",
                    cabecalho=cabecalho,
                    rodape=rodape
                )

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )


def send_notification_servicos_em_andamento_limpeza_predial(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteLimpezaPredial.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
            configuracoes = SettingServicosGerenteLimpezaPredial.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosEmAndamento == True:
                em_andamento = query_servicos_limpeza_predial_agendados_anotados(
                    request,
                    '3y4RzZT5KxWQ',
                    status_list=['Agendado', 'Em andamento']
                ).filter(
                    novo_status='Em andamento'
                )

                cabecalho = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Serviços atrasados, sua organização possui {len(em_andamento)} serviços em andamento, considere conclui-los</br>
                </div>"""

                rodape = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Sua organização não possui serviço(s) em andamento</br>
                </div>"""

                send_notification_limpeza_predial(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=em_andamento,
                    colunas=colunas_limpeza_predial,
                    assunto="Limpeza predial | Serviços em andamento",
                    cabecalho=cabecalho,
                    rodape=rodape
                )

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )
