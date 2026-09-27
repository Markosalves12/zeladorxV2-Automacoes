from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from servicos.models_limpeza_predial import ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado
from areas.models_limpeza_predial import AreaLimpezaPredial
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial


def agendar_servicos_limpeza_predial_configurados():
    objects = ServicoLimpezaPredialConfigurado.objects.filter(
        status='Mobilizado',
        Areas__status='Mobilizado',
        Areas__localidade__status='Mobilizado',
        Areas__localidade__unidade__status='Mobilizado',
        ServicosEscalados__status='Mobilizado'
    ).distinct()

    dias_semana_portugues = {
        'Monday': 'Segunda-Feira',
        'Tuesday': 'Terça-Feira',
        'Wednesday': 'Quarta-Feira',
        'Thursday': 'Quinta-Feira',
        'Friday': 'Sexta-Feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    dia_atual_semana = datetime.now().strftime('%A')

    # Filtrar apenas os serviços programados para o dia atual
    objects = objects.filter(diasaseremrealizado__diasdasemana=dias_semana_portugues[dia_atual_semana])

    for obj in objects:
        try:
            area = AreaLimpezaPredial.objects.get(id_random=obj.Areas.id_random)
        except AreaLimpezaPredial.DoesNotExist:
            # print(f"Área com id_random {obj.Areas.id_random} não encontrada. Pulando...")
            continue

        ServicosEscalados = CatalogodeServicoLimpezaPredial.objects.filter(
            id_random__in=[servico.id_random for servico in obj.ServicosEscalados.all()],
            status='Mobilizado'
        )

        if not ServicosEscalados.exists():
            # print(f"Objeto {obj.id_random} não possui serviços escalados mobilizados. Pulando...")
            continue

        idconfigurate = obj.id_random
        tempomedioplanejado = obj.tempomedioplanejado or timedelta(minutes=30)

        horarios = [h for h in [
            obj.horario_1, obj.horario_2, obj.horario_3,
            obj.horario_4, obj.horario_5, obj.horario_6, obj.horario_7
        ] if h]

        if not horarios:
            # print(f"Objeto {obj.id_random} não possui horários válidos. Pulando...")
            continue

        for horario in horarios:
            data_atual = datetime.now().date()
            data_inicio = make_aware(datetime.combine(data_atual, horario))
            data_conclusao = data_inicio + tempomedioplanejado

            new_service_scheduled = ServicoLimpezaPredialAgendado(
                id_configuracao=idconfigurate,
                DescricaoDoServico=", ".join(servicoescalado.nome for servicoescalado in ServicosEscalados)[:199],
                Areas=area,
                DataDeInicio=data_inicio,
                DataDeConclusao=data_conclusao,
                TipoServico='Automático',
            )

            new_service_scheduled.save()
            new_service_scheduled.ServicosEscalados.set(ServicosEscalados)

            # print(f"Serviço de limpeza predial agendado para {data_inicio} na área {area.id_random}")
