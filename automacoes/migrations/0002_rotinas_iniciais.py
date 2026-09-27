from datetime import time

from django.db import migrations

ROTINAS = [
    ('gerar_jardinagem', 'Gerar serviços de Jardinagem', time(0, 15), 10,
     'Cria os serviços automáticos do dia a partir das configurações de Jardinagem (substitui a rota force_updates/).'),
    ('gerar_limpeza_predial', 'Gerar serviços de Limpeza Predial', time(0, 15), 20,
     'Cria os serviços automáticos do dia a partir das configurações de Limpeza Predial (substitui a rota force_updates/).'),
    ('email_resumo_diario', 'Resumo diário por e-mail', time(6, 30), 30,
     'Envia a cada gerente a lista de serviços previstos para o dia nas suas equipes.'),
    ('email_atrasados', 'Alerta de serviços atrasados', time(9, 0), 40,
     'Avisa os gerentes sobre serviços que passaram do prazo nos últimos 7 dias e não foram concluídos.'),
    ('email_concluidos', 'Resumo de serviços concluídos', time(18, 0), 50,
     'Envia aos gerentes das empresas atendidas o que foi concluído no dia.'),
]


def criar(apps, schema_editor):
    Rotina = apps.get_model('automacoes', 'Rotina')
    for codigo, nome, horario, ordem, descricao in ROTINAS:
        Rotina.objects.get_or_create(codigo=codigo, defaults={
            'nome': nome, 'horario': horario, 'ordem': ordem, 'descricao': descricao, 'frequencia': 'diaria',
        })


class Migration(migrations.Migration):
    dependencies = [('automacoes', '0001_initial')]
    operations = [migrations.RunPython(criar, migrations.RunPython.noop)]
