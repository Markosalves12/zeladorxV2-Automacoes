from django.shortcuts import render
from notifications.utils_jardinagem import send_notification_jardinagem, colunas_retorno_proximo, colunas_jardinagem
from servicos.utils_jardinagem import query_servicos_jardinagem_agendados_anotados
from settings.models import SettingServicosGerenteJardinagem
from empresasecundario.utils import define_empresas
from django.db.models import F, Value, CharField, Case, When, IntegerField, DateField, DateTimeField, Q
from django.db.models import ExpressionWrapper, DurationField
from django.utils import timezone
from django.db.models.functions import ExtractDay

def send_notification_servicos_atrasados_jardinagem(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteJardinagem.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
            configuracoes = SettingServicosGerenteJardinagem.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosAtrasados == True:
                atrasados = query_servicos_jardinagem_agendados_anotados(
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

                send_notification_jardinagem(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=atrasados,
                    colunas=colunas_jardinagem,
                    assunto="Jardinagem | Serviços atrasados",
                    cabecalho=cabecalho,
                    rodape=rodape,
                )


    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )


def send_notification_servicos_proximos_jardinagem(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteJardinagem.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
            configuracoes = SettingServicosGerenteJardinagem.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosProximos == True:
                proximos = query_servicos_jardinagem_agendados_anotados(
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

                send_notification_jardinagem(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=proximos,
                    colunas=colunas_jardinagem,
                    assunto="Jardinagem | Serviços próximos",
                    cabecalho=cabecalho,
                    rodape=rodape
                )

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )


def send_notification_servicos_em_andamento_jardinagem(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteJardinagem.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
            configuracoes = SettingServicosGerenteJardinagem.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosEmAndamento == True:
                em_andamento = query_servicos_jardinagem_agendados_anotados(
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

                send_notification_jardinagem(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=em_andamento,
                    colunas=colunas_jardinagem,
                    assunto="Jardinagem | Serviços em andamento",
                    cabecalho=cabecalho,
                    rodape=rodape
                )

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )



def send_notificaton_retorno_proximo(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteJardinagem.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
            configuracoes = SettingServicosGerenteJardinagem.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosProximos == True:
                # Dias desde o atendimento até agora
                proximos = query_servicos_jardinagem_agendados_anotados(
                    request,
                    userid=Gerente.id_random,
                    status_list=['Concluido']
                ).distinct('Areas__id_random').order_by('Areas__id_random', '-DataDeConclusao').annotate(
                    dias_diferenca=ExpressionWrapper(
                        timezone.now() - F('DataDeConclusao'),
                        output_field=DurationField()
                    ),
                    Periodicidade=ExpressionWrapper(
                        F('Areas__periodicidade'),
                        output_field=CharField()
                    )
                ).filter(
                    Areas__status='Mobilizado'
                )

                # Aplicar filtros diretamente no queryset
                proximos = proximos.annotate(
                    data_retorno=ExpressionWrapper(
                        F('DataDeConclusao') +
                        Case(
                            When(Periodicidade='Quinzenal', then=timezone.timedelta(days=15)),
                            When(Periodicidade='Mensal', then=timezone.timedelta(days=30)),
                            When(Periodicidade='Bimestral', then=timezone.timedelta(days=60)),
                            When(Periodicidade='Trimestral', then=timezone.timedelta(days=90)),
                            When(Periodicidade='Semestral', then=timezone.timedelta(days=180)),
                            When(Periodicidade='Anual', then=timezone.timedelta(days=365)),
                            default=timezone.timedelta(days=0),
                            output_field=DurationField()
                        ),
                        output_field=DateTimeField()
                    ),
                    dias_restantes=ExpressionWrapper(
                        F('data_retorno') - timezone.now(),
                        output_field=DurationField()
                    )
                ).annotate(
                    dias_restantes_num=ExtractDay(F('dias_restantes'))
                ).filter(
                    Q(Periodicidade='Quinzenal', dias_restantes_num__lte=3, dias_restantes_num__gte=0) |
                    Q(Periodicidade='Mensal', dias_restantes_num__lte=7, dias_restantes_num__gte=0) |
                    Q(Periodicidade='Bimestral', dias_restantes_num__lte=15, dias_restantes_num__gte=0) |
                    Q(Periodicidade='Trimestral', dias_restantes_num__lte=15, dias_restantes_num__gte=0) |
                    Q(Periodicidade='Semestral', dias_restantes_num__lte=20, dias_restantes_num__gte=0) |
                    Q(Periodicidade='Anual', dias_restantes_num__lte=30, dias_restantes_num__gte=0)
                )

                # Adicionar formatação para exibição
                for obj in proximos:
                    obj.data_retorno_formatada = obj.data_retorno.strftime('%d/%m/%Y')
                    obj.dias_restantes = obj.dias_restantes_num

                cabecalho = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Retorno programado as áreas se aproximando, sua organização possui {len(proximos)} serviços para serem remarcados em alguns dias</br>
                </div>"""

                rodape = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Sua organização não possui retornos programados se aproximando</br>
                </div>"""

                send_notification_jardinagem(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=proximos,
                    colunas=colunas_retorno_proximo,
                    assunto="Jardinagem | Retornos programados se aproximando",
                    cabecalho=cabecalho,
                    rodape=rodape
                )

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )


def send_notificaton_retorno_atrasado(request):
    # SettingServicosGerenteJardinagem model contendo as configuracoes salvas pelos gerentes
    for value in SettingServicosGerenteJardinagem.objects.all():
        # acessa o gerente via chave estrangeira no model. onde a coluna Gerente de SettingServicosGerenteJardinagem, armazena os dados de gerentes
        Gerente = value.Gerente
        # gerente desmobilizados nao recebem notificacoes
        if Gerente.status == "Desmobilizado":
            continue

        empresas = define_empresas(request=request, userid=Gerente.id_random)
        setores = empresas['setores']

        # o macro servico de jardinagem precisa esta habilitado para receber notificaceos
        if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
            configuracoes = SettingServicosGerenteJardinagem.objects.get(Gerente=Gerente)

            if configuracoes.NotificationsServicosProximos == True:
                # Dias desde o atendimento até agora
                proximos = query_servicos_jardinagem_agendados_anotados(
                    request,
                    userid=Gerente.id_random,
                    status_list=['Concluido']
                ).distinct('Areas__id_random').order_by('Areas__id_random', '-DataDeConclusao').annotate(
                    dias_diferenca=ExpressionWrapper(
                        timezone.now() - F('DataDeConclusao'),
                        output_field=DurationField()
                    ),
                    Periodicidade=ExpressionWrapper(
                        F('Areas__periodicidade'),
                        output_field=CharField()
                    )
                ).filter(
                    Areas__status='Mobilizado'
                )

                # Aplicar filtros diretamente no queryset
                proximos = proximos.annotate(
                    data_retorno=ExpressionWrapper(
                        F('DataDeConclusao') +
                        Case(
                            When(Periodicidade='Quinzenal', then=timezone.timedelta(days=15)),
                            When(Periodicidade='Mensal', then=timezone.timedelta(days=30)),
                            When(Periodicidade='Bimestral', then=timezone.timedelta(days=60)),
                            When(Periodicidade='Trimestral', then=timezone.timedelta(days=90)),
                            When(Periodicidade='Semestral', then=timezone.timedelta(days=180)),
                            When(Periodicidade='Anual', then=timezone.timedelta(days=365)),
                            default=timezone.timedelta(days=0),
                            output_field=DurationField()
                        ),
                        output_field=DateTimeField()
                    ),
                    dias_restantes=ExpressionWrapper(
                        F('data_retorno') - timezone.now(),
                        output_field=DurationField()
                    )
                ).annotate(
                    dias_restantes_num=ExtractDay(F('dias_restantes'))
                ).filter(
                    Q(Periodicidade='Quinzenal', dias_restantes_num__lt=0) |
                    Q(Periodicidade='Mensal', dias_restantes_num__lt=0) |
                    Q(Periodicidade='Bimestral', dias_restantes_num__lt=0) |
                    Q(Periodicidade='Trimestral', dias_restantes_num__lt=0) |
                    Q(Periodicidade='Semestral', dias_restantes_num__lt=0) |
                    Q(Periodicidade='Anual', dias_restantes_num__lt=0)
                )

                # Adicionar formatação para exibição
                for obj in proximos:
                    obj.data_retorno_formatada = obj.data_retorno.strftime('%d/%m/%Y')
                    obj.dias_restantes = obj.dias_restantes_num

                cabecalho = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Retorno programado as áreas atrasados, sua organização possui {len(proximos)} serviços para serem remarcados</br>
                </div>"""

                rodape = f"""<div>
                    Ola! {Gerente.username}, tudo bem? </br>
                    Sua organização não possui retornos programados em atraso</br>
                </div>"""

                send_notification_jardinagem(
                    request=request,
                    userid=Gerente.id_random,
                    email=Gerente.email,
                    username=Gerente.username,
                    dados=proximos,
                    colunas=colunas_retorno_proximo,
                    assunto="Jardinagem | Retornos programados em atraso",
                    cabecalho=cabecalho,
                    rodape=rodape
                )

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )