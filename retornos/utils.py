from datetime import timedelta
from django.utils import timezone

PERIODICIDADE_DIAS = {
    'Semanal': 7,
    'Quinzenal': 15,
    'Mensal': 30,
    'Bimestral': 61,     # 30.5 * 2
    'Trimestral': 91,    # 30.5 * 3
    'Semestral': 183,    # 30.5 * 6
    'Anual': 365
}

def calcular_data_retorno_formatada(data_conclusao, periodicidade):
    dias_periodo = PERIODICIDADE_DIAS.get(periodicidade)
    if not data_conclusao or not dias_periodo:
        return ("Indefinido", None)

    data_retorno = data_conclusao + timedelta(days=dias_periodo)
    dias_restantes = (data_retorno - timezone.now().date()).days
    data_formatada = data_retorno.strftime('%d/%m/%Y')

    return data_formatada, dias_restantes

def formatar_tempo_desde(duracao: timedelta):
    if not duracao:
        return "Desconhecido"

    dias = duracao.days

    if dias < 30:
        return f"{dias} dias"
    elif dias < 365:
        meses = int(dias // 30.5)
        dias_restantes = int(dias % 30.5)
        if meses == 1:
            return f"{meses} mês e {dias_restantes} dias"
        return f"{meses} meses e {dias_restantes} dias"
    else:
        meses = int(dias // 30.5)
        dias_restantes = int(dias % 30.5)
        return f"{meses} meses e {dias_restantes} dias"