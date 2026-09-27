from relatorios.utils_pdf_json import relatorio_pdf_json
from checklists.models import CheckListJardinagem
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings
from relatorios.utils_pdf import (agrupar_execucoes_por_agendamento, draw_footer, draw_header, add_figures_to_pdf, draw_status_with_background,
                                  draw_checklist_table, draw_execution_table, draw_all_images_intercalated)
from utils.utils import generate_id_random, filtrar_unicos
from datetime import datetime
from relatorios.jardinagem.utils import (graphs_jardinagem_proximo_to_reports,
                                         graphs_jardinagem_atrasado_to_reports,
                                         graphs_jardinagem_agendado_to_reports,
                                         graphs_jardinagem_em_andamento_to_reports,
                                         graphs_jardinagem_concluido_to_reports)
from permissionscontrol.utils import verify_login
from django.shortcuts import redirect
from servicos.utils_jardinagem import colect_dados_fato_servico_jardinagem, query_servicos_jardinagem_agendados_anotados
from relatorios.utils import define_filters

def exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
                                                               TipoServico, ServicosEscalados, ColaboradoresEscalados):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    DataDeInicio = datetime.strptime(DataDeInicio, '%Y-%m-%dT%H:%M') if DataDeInicio and DataDeInicio != "None" else 'None'
    DataDeConclusao = datetime.strptime(DataDeConclusao, '%Y-%m-%dT%H:%M') if DataDeConclusao and DataDeConclusao != "None" else 'None'
    ServicosEscalados = ServicosEscalados.split(',')
    ColaboradoresEscalados = ColaboradoresEscalados.split(',')

    filters = define_filters(
        DataDeInicio=DataDeInicio,
        DataDeConclusao=DataDeConclusao,
        TipoServico=TipoServico,
        Areas=Areas,
        ServicosEscalados=ServicosEscalados,
        ColaboradoresEscalados=ColaboradoresEscalados
    )

    dados = query_servicos_jardinagem_agendados_anotados(
        request,
        userid,
        ['Agendado', 'Em andamento', 'Concluido']
    ).filter(
        status__in=status.split(',')
    )
    dados = filtrar_unicos(dados, **filters)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    x = 50

    # função que cria o cabeçalho propriamente falado
    # Draw the header for the first page
    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    y = height - 120
    page_number = 1
    p.setFont("Helvetica", 10)

    # Carrega relacionamentos de uma vez e busca os acompanhamentos em uma única consulta
    dados = dados.select_related('Areas').prefetch_related('ServicosEscalados', 'ColaboradoresEscalados')
    execucoes_por_agendamento = agrupar_execucoes_por_agendamento(colect_dados_fato_servico_jardinagem(
        request=request,
        userid=userid,
        DataDeInicio=DataDeInicio,
        DataDeConclusao=DataDeConclusao,
        ServicosEscalados=ServicosEscalados,
        ColaboradoresEscalados=ColaboradoresEscalados,
        TipoServico=TipoServico,
        Areas=Areas,
        status=status.split(',')
    ), dados)

    # PDF montado no navegador: devolve os mesmos dados em JSON
    if request.GET.get('formato') == 'json':
        return relatorio_pdf_json(dados, execucoes_por_agendamento, permission_type='jardinagem', status=status, checklist_model=CheckListJardinagem)

    if len(dados) > 0:
        for dado in dados:
            y = draw_status_with_background(p, x, y, dado, dado.dias_diferenca, permission_type="jardinagem")

            y = draw_all_images_intercalated(
                p,
                x,
                y,
                width,
                height,
                dado,
                header_image_path,
                checklist_model=CheckListJardinagem
            )

            # Adicionar tabela de dados de execução após a foto de conclusão
            execucao_dados = execucoes_por_agendamento.get(dado.id, [])

            # Desenhar a tabela de execução
            y, page_number = draw_execution_table(
                p=p,
                x=x,
                y=y,
                width=width,
                height=height,
                execucao_dados=execucao_dados,
                header_image_path=header_image_path,
                page_number=page_number
            )

            # Adicionar tabela de checklist após a tabela de execução
            y = draw_checklist_table(p, x, y, width, height, dado, CheckListJardinagem, header_image_path)

            draw_footer(p, width)
            p.showPage()
            page_number += 1
            p.setFont("Helvetica", 10)
            y = height - 70

    else:
        p.showPage()
        page_number += 1
        p.setFont("Helvetica", 10)
        y = height - 70

    start_y = height - 100
    p.setFont('Helvetica-Bold', 12)

    if 'Concluido' in status.split(',') and len(dados) > 0:
        (figs_concluidos_terreno, figs_concluidos_vegetacao, figs_concluidos_localidade,
         figs_concluidos_area, figs_concluidos_colaborador,
         figs_concluidos_servico) = graphs_jardinagem_concluido_to_reports(request, userid, dados)

        p.drawString(50, start_y, f"Volume de serviços prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p,
            {
                **figs_concluidos_terreno,
                **figs_concluidos_vegetacao,
                **figs_concluidos_localidade,
                **figs_concluidos_area,
                **figs_concluidos_colaborador,
                **figs_concluidos_servico
            },
            start_y,
            start_y + 1,
            header_image_path=header_image_path,
            width=width,
            height=height
        )

    else:
        graps_to_report = {}

        if len(dados.filter(novo_status='Próximo')) > 0:
            (figs_proximo_terreno, figs_proximo_vegetacao, figs_proximo_localidade, figs_proximo_area,
             figs_proximo_colaborador, figs_proximo_servico) = graphs_jardinagem_proximo_to_reports(request, userid, dados)
            graps_to_report.update(**figs_proximo_terreno, **figs_proximo_vegetacao, **figs_proximo_localidade,
                                   **figs_proximo_area, **figs_proximo_colaborador, **figs_proximo_servico)

        if len(dados.filter(novo_status='Atrasado')) > 0:
            (figs_atrasados_terreno, figs_atrasados__vegetacao, figs_atrasados__localidade, figs_atrasados__area,
             figs_atrasados__colaborador, figs_atrasados__servico) = graphs_jardinagem_atrasado_to_reports(request, userid, dados)
            graps_to_report.update(**figs_atrasados_terreno, **figs_atrasados__vegetacao, **figs_atrasados__localidade,
                                   **figs_atrasados__area, **figs_atrasados__colaborador, **figs_atrasados__servico)

        if len(dados.filter(novo_status='Agendado')) > 0:
            (figs_agendado_terreno, figs_agendado_vegetacao, figs_agendado_localidade,
             figs_agendado_area, figs_agendado_colaborador,
             figs_agendado_servico) = graphs_jardinagem_agendado_to_reports(request, userid, dados)
            graps_to_report.update(**figs_agendado_terreno, **figs_agendado_vegetacao, **figs_agendado_localidade,
                                   **figs_agendado_area, **figs_agendado_colaborador, **figs_agendado_servico)

        if len(dados.filter(novo_status='Em andamento')) > 0:
            (figs_em_andamento_terreno, figs_em_andamento_vegetacao, figs_em_andamento_localidade,
             figs_em_andamento_area, figs_em_andamento_colaborador,
             figs_em_andamento_servico) = graphs_jardinagem_em_andamento_to_reports(request, userid, dados)
            graps_to_report.update(**figs_em_andamento_terreno, **figs_em_andamento_vegetacao,
                                   **figs_em_andamento_localidade,
                                   **figs_em_andamento_area, **figs_em_andamento_colaborador,
                                   **figs_em_andamento_servico)

        p.drawString(50, start_y, f"Volume de serviços Agendados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(p, graps_to_report, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height)

    draw_footer(p, width, is_last_page=True)
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {status} {generate_id_random()}.pdf"'
    return response