from relatorios.utils_pdf_json import relatorio_pdf_json
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings
from utils.utils import generate_id_random, define_range_time, filtrar_unicos
from relatorios.utils_pdf import (agrupar_execucoes_por_agendamento, draw_footer, draw_header, add_figures_to_pdf, draw_status_with_background,
                                  draw_request_and_delivery_images, draw_execution_table)
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial, query_servicos_limpeza_predial_agendados_anotados
from relatorios.limpeza_predial.utils import (graphs_limpeza_predial__proximo_to_reports,
                                              graphs_limpeza_predial_atrasado_to_reports,
                                              graphs_limpeza_predial_agendado_to_reports,
                                              graphs_limpeza_predial_em_andamento_to_reports,
                                              graphs_limpeza_predial_concluido_to_reports)
from datetime import datetime
from django.shortcuts import redirect
from permissionscontrol.utils import verify_login
from relatorios.utils import define_filters

def exportar_relatorio_de_serivos_limpeza_predial_pdf(request, userid, status, DataDeInicio, DataDeConclusao, Areas,
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

    dados = query_servicos_limpeza_predial_agendados_anotados(
        request,
        userid,
        ['Agendado', 'Em andamento', 'Concluido']
    ).filter(
        status__in=status.split(',')
    )
    dados = filtrar_unicos(dados, **filters)

    # cria um buffer para inserir os dados no pdf
    buffer = BytesIO()
    # cria um objeto pdf usando o buffer anterior
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # defini a posição inicial do cursor
    x = 50

    # função que cria o cabeçalho propriamente falado
    # Draw the header for the first page
    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    y = height - 120  # Adjust starting position for content after the header
    page_number = 1
    p.setFont("Helvetica", 10)

    # Carrega relacionamentos de uma vez e busca os acompanhamentos em uma única consulta
    dados = dados.select_related('Areas').prefetch_related('ServicosEscalados')
    execucoes_por_agendamento = agrupar_execucoes_por_agendamento(colect_dados_fato_servico_limpeza_predial(
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
        return relatorio_pdf_json(dados, execucoes_por_agendamento, permission_type='limpeza_predial', status=status)

    if len(dados) > 0:
        for dado in dados:
            y = draw_status_with_background(p, x, y, dado, dado.dias_diferenca)

            # Adicionar dados de execução como tabela
            execucao_dados = execucoes_por_agendamento.get(dado.id, [])

            for execucao_dado in execucao_dados:
                y = draw_request_and_delivery_images(p, x, y, width, height, execucao_dado, header_image_path)

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

            # Draw the footer on the current page
            draw_footer(p, width)
            p.showPage()
            page_number += 1
            p.setFont("Helvetica", 10)  # Reset font size to 12 for new page content
            y = height - 70

    else:
        p.showPage()
        page_number += 1
        p.setFont("Helvetica", 10)  # Reset font size to 12 for new page content
        y = height - 70

    start_y = height - 100  # Posição inicial para o conteúdo após o cabeçalho
    p.setFont('Helvetica-Bold', 12)

    if 'Concluido' in status.split(',') and len(dados)>0:
        (figs_concluidos_localidade,
         figs_concluidos_area,
         figs_concluidos_servico) = graphs_limpeza_predial_concluido_to_reports(request, userid, dados)

        p.drawString(50, start_y, f"Volume de servicos prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, {
                **figs_concluidos_localidade,
                **figs_concluidos_area,
                **figs_concluidos_servico
            }, start_y,
            start_y + 1,
            header_image_path=header_image_path,
            width=width,
            height=height
        )

    else:
        one_day, seven_days = define_range_time()

        graps_to_report = {}

        if len(dados.filter(novo_status='Próximo')) > 0:
            (figs_proximo_localidade,figs_proximo_area,
             figs_proximo_servico,) = graphs_limpeza_predial__proximo_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_proximo_localidade,
                **figs_proximo_area,
                **figs_proximo_servico,
            )

        if len(dados.filter(novo_status='Atrasado')) > 0:
            (figs_atrasados__localidade, figs_atrasados__area,
             figs_atrasados__servico,) = graphs_limpeza_predial_atrasado_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_atrasados__localidade,
                **figs_atrasados__area,
                **figs_atrasados__servico,
            )

        if len(dados.filter(novo_status='Agendado')) > 0:
            (figs_agendado_localidade,
             figs_agendado_area, figs_agendado_servico) = graphs_limpeza_predial_agendado_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_agendado_localidade,
                **figs_agendado_area,
                **figs_agendado_servico,
            )

        if len(dados.filter(novo_status='Em andamento')) > 0:
            (figs_em_andamento_localidade,
             figs_em_andamento_area, figs_em_andamento_servico) = graphs_limpeza_predial_em_andamento_to_reports(request, userid, dados)

            graps_to_report.update(
                **figs_em_andamento_localidade,
                **figs_em_andamento_area,
                **figs_em_andamento_servico
            )

        p.drawString(50, start_y, f"Volume de servicos prestados")
        start_y -= 20
        start_y, end_page = add_figures_to_pdf(
            p, graps_to_report, start_y, start_y + 1, header_image_path=header_image_path, width=width, height=height
        )

    draw_footer(
        p,
        width,
        is_last_page=True
    )

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    buffer.seek(0)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos {status} {generate_id_random()}.pdf"'

    return response