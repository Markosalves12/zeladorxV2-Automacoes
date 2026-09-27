from relatorios.utils_pdf_json import relatorio_pdf_json
from servicos.utils_limpeza_predial import colect_dados_fato_servico_limpeza_predial, query_servicos_limpeza_predial_agendados_anotados
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.conf import settings
from utils.utils import generate_id_random, filtrar_unicos
from relatorios.utils_pdf import (agrupar_execucoes_por_agendamento, draw_footer, draw_header, add_figures_to_pdf, draw_status_with_background,
                                  draw_request_and_delivery_images, draw_execution_table)
from relatorios.limpeza_predial.utils import graphs_limpeza_predial_concluido_to_reports
from areas.models_limpeza_predial import AreaLimpezaPredial
from datetime import datetime
from django.shortcuts import redirect
from permissionscontrol.utils import verify_login
from relatorios.utils import define_filters

def exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf(request, userid, id_random, DataDeInicio,
                                                              DataDeConclusao, Areas, TipoServico, ServicosEscalados,
                                                              ColaboradoresEscalados, type):
    block = verify_login(request=request, userid=userid)

    if block:
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
        status__in=['Concluido']
    )
    dados = filtrar_unicos(dados, **filters)

    if type == 'catalogo_de_servicos':
        dados = filtrar_unicos(dados, ServicosEscalados__id_random=id_random)
    elif type == 'configuracao':
        dados = dados.filter(id_configuracao=id_random)

    elif type == 'areas':
        dados = dados.filter(Areas__id_random=id_random)

    elif type == 'gerente':
        execucao_dados = colect_dados_fato_servico_limpeza_predial(
            request=request,
            userid=userid,
            DataDeInicio=DataDeInicio,
            DataDeConclusao=DataDeConclusao,
            ServicosEscalados=ServicosEscalados,
            ColaboradoresEscalados=ColaboradoresEscalados,
            TipoServico=TipoServico,
            Areas=Areas,
            status=['Concluido']
        ).filter(
            colaboradores_chamados_id_random=id_random
        )

        # Obter todos os IDs únicos de uma vez
        ids_random_agendamentos = {dado.id_random_agendamento for dado in execucao_dados}

        # Filtrar todos os dados de uma vez
        dados = dados.filter(id_random__in=ids_random_agendamentos)

    # Create PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    x = 50

    # Draw header
    header_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/logo alt.png')
    draw_header(c=p, header_image_path=header_image_path, width=width, height=height)

    y = height - 120  # Starting position after header
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
        status=['Concluido']
    ), dados)

    # PDF montado no navegador: devolve os mesmos dados em JSON
    if request.GET.get('formato') == 'json':
        return relatorio_pdf_json(dados, execucoes_por_agendamento, permission_type='limpeza_predial', status=['Concluido'])

    if len(dados) > 0:
        for dado in dados:
            y = draw_status_with_background(p, x, y, dado, dado.dias_diferenca)

            # Adicionar dados de execução como tabela após as imagens
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

            # Draw footer and start new page
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

    if len(dados) > 0:
        (figs_concluidos_localidade,
         figs_concluidos_area,
         figs_concluidos_servico) = graphs_limpeza_predial_concluido_to_reports(request, userid, dados)

        start_y = height - 100
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, start_y, "Volume de serviços concluídos")
        start_y -= 20

        start_y, end_page = add_figures_to_pdf(
            p,
            {
                **figs_concluidos_localidade,
                **figs_concluidos_area,
                **figs_concluidos_servico
            },
            start_y,
            start_y + 1,
            header_image_path=header_image_path,
            width=width,
            height=height
        )

    draw_footer(p, width, is_last_page=True)
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio de servicos Concluido {generate_id_random()}.pdf"'

    return response