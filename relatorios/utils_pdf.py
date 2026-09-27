from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
import plotly.io as pio
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from utils.utils import formatar_atributos

def calculate_new_dimensions(img_width, img_height):
    new_width = img_width / 2
    new_height = img_height / 2
    return new_width, new_height


# Lado máximo (em pixels) das fotos embutidas no PDF. As fotos continuam sendo
# desenhadas no mesmo tamanho de antes; apenas a resolução interna é reduzida,
# o que deixa a geração e o download do relatório muito mais rápidos.
PDF_IMAGE_MAX_SIDE = 1000
PDF_IMAGE_CACHE_LIMIT = 64
_pdf_image_cache = {}


def _image_cache_key(image_source):
    name = getattr(image_source, 'name', None)
    return name if name else str(image_source)


def load_pdf_image(image_source):
    """
    Carrega uma imagem (caminho local ou arquivo do storage), reduz a resolução
    e devolve (ImageReader, largura_original, altura_original).
    O resultado fica em cache para não baixar/decodificar a mesma imagem várias vezes.
    """
    key = _image_cache_key(image_source)
    if key in _pdf_image_cache:
        return _pdf_image_cache[key]

    from PIL import Image
    from io import BytesIO

    if hasattr(image_source, 'open') and not isinstance(image_source, str):
        image_source.open('rb')
        try:
            raw = BytesIO(image_source.read())
        finally:
            image_source.close()
        img = Image.open(raw)
    else:
        img = Image.open(image_source)

    original_width, original_height = img.size

    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail((PDF_IMAGE_MAX_SIDE, PDF_IMAGE_MAX_SIDE))
    compressed = BytesIO()
    img.save(compressed, format='JPEG', quality=75, optimize=True)
    compressed.seek(0)

    result = (ImageReader(compressed), original_width, original_height)
    if len(_pdf_image_cache) >= PDF_IMAGE_CACHE_LIMIT:
        _pdf_image_cache.pop(next(iter(_pdf_image_cache)))
    _pdf_image_cache[key] = result
    return result


def draw_image(image_path, x, y, p):
    try:
        img_data, img_width, img_height = load_pdf_image(image_path)
        new_width, new_height = calculate_new_dimensions(img_width, img_height)
        p.drawImage(img_data, x, y - new_height, width=new_width, height=new_height, mask='auto')
        return new_height
    except Exception as e:
        p.drawString(x, y, f"Erro ao carregar a imagem: {str(e)}")
        return 0


def agrupar_execucoes_por_agendamento(execucoes, dados):
    """
    Busca os acompanhamentos uma única vez e agrupa por agendamento,
    sem repetir o mesmo acompanhamento (id único).
    """
    ids_agendamentos = {dado.id for dado in dados}
    agrupados = {}
    vistos = set()
    for execucao in execucoes.filter(id_agendamento__in=ids_agendamentos).order_by('id'):
        if execucao.id in vistos:
            continue
        vistos.add(execucao.id)
        agrupados.setdefault(execucao.id_agendamento, []).append(execucao)
    return agrupados


def carregar_checklists(dado, checklist_model):
    """Checklist do agendamento, consultado uma única vez por serviço."""
    cache = getattr(dado, '_checklists_pdf', None)
    if cache is None:
        cache = list(
            checklist_model.objects.filter(servico_agendado__id=dado.id)
            .select_related('servico_agendado').distinct().order_by('id')
        )
        dado._checklists_pdf = cache
    return cache


def draw_footer(c, width, is_last_page=False):
    c.setFont("Helvetica", 9)
    if is_last_page:
        last_page_text = "zeladorX"
        c.drawString((width - c.stringWidth(last_page_text, fontSize=12)) / 2, 50, last_page_text)

def save_plotly_fig_as_image(fig, file_path=None):
    """Converte a figura Plotly em PNG na memória (sem gravar em disco)."""
    from io import BytesIO
    return BytesIO(pio.to_image(fig, format='png'))

_header_cache = {}


def draw_header(c, header_image_path, width, height):
    # se o endereço da imagem existir
    if os.path.exists(header_image_path):
        # abri a imagem enviada como parametro
        header_image = _header_cache.get(header_image_path)
        if header_image is None:
            header_image = ImageReader(header_image_path)
            _header_cache[header_image_path] = header_image
        # captura as dimensões da imagem
        header_img_width, header_img_height = header_image.getSize()
        # centraliza a imagem no topo
        x_centered = (width - header_img_width / 3) / 2
        c.drawImage(header_image, x_centered, height - header_img_height / 3 - 20, width=header_img_width / 3, height=header_img_height / 3, mask='auto')
        image_bottom = height - header_img_height / 2 - 20 - header_img_height / 2 - 20
    else:
        image_bottom = height  # Adjust if image is not found

    # Adiciona o titulo do relatório abaixo da imagem

    # configura da fonte e tamanho do titulo
    # c.setFont("Helvetica-Bold", 16)
    c.setFont("Helvetica-Bold", 14)
    # escrever o titulo do relatório
    c.drawString((width - c.stringWidth(f"Relatório de Serviços",
                                        "Helvetica-Bold", fontSize=12)) / 2,
                 image_bottom + 50, f"Relatório de Serviços")

    c.drawString((width - c.stringWidth(f"",
                                        "Helvetica-Bold", fontSize=12)) / 2,
                 image_bottom + 0,
                 f"")

    c.drawString((width - c.stringWidth(f"",
                                        "Helvetica-Bold", fontSize=12)) / 2,
                 image_bottom - 20,
                 f"")

    c.setFont("Helvetica", 12)  # Set font back to normal for the rest of the content


def add_figures_to_pdf(c, fig_dict, start_y, start_page, width, height, header_image_path):
    width, height = letter
    y = start_y
    page_number = start_page

    for fig_name, fig_html in fig_dict.items():
        fig_buffer = save_plotly_fig_as_image(fig_html)

        if fig_buffer:
            fig_image = ImageReader(fig_buffer)
            fig_img_width, fig_img_height = fig_image.getSize()
            if y - fig_img_height / 3 < 50:
                draw_footer(c, page_number, is_last_page=False)
                c.showPage()
                page_number += 1
                # draw_header(c, header_image_path, width, height)
                y = height - 150

            n = 2
            c.drawImage(fig_image, (width - fig_img_width / n) / 2, y - fig_img_height / n,
                        width=fig_img_width / n, height=fig_img_height / n, mask='auto')
            y -= fig_img_height / n + 20

    return y, page_number


def draw_status_with_background(p, x, y, dado, dias_diferenca, permission_type=None):
    """
    Desenha o texto com o status colorido e informações iniciais no PDF.

    Args:
        p: Objeto canvas do ReportLab (para desenhar no PDF).
        x: Posição x inicial do texto.
        y: Posição y inicial do texto.
        dado: Objeto contendo DescricaoDoServico, id, status, novo_status, DataDeInicio,
              DataDeConclusao, Areas, ServicosEscalados e ColaboradoresEscalados.
        dias_diferenca: Valor numérico para determinar o status com base em dias.

    Returns:
        y: Nova posição y após desenhar todo o texto.
    """
    # Configurações iniciais para o status
    p.setFont('Helvetica-Bold', 10)
    description_part = f"Descrição: {dado.DescricaoDoServico} (Agendamento.Id: {dado.id}) "
    description_width = p.stringWidth(description_part, 'Helvetica-Bold', 10)
    status_x = x + description_width  # Posição onde o status começa

    # Determinar o status a ser exibido e suas cores
    background_color = None
    text_color = None
    status_text = None
    status_width = None
    status_height = 12  # Altura fixa do fundo colorido

    # Regras de cores baseadas no status
    status_rules = {
        "Em andamento": {"background": "#008000", "text": "#FFFFFF"},  # Verde, texto branco
        "Cancelado": {"background": "#808080", "text": "#FFFFFF"},     # Cinza, texto branco
        "Concluido": {"background": "#020d3f", "text": "#FFFFFF"},    # Azul escuro, texto branco
    }

    # Verificar primeiro as condições baseadas em dado.status
    if dado.status in status_rules:
        status_text = str(dado.status)
        background_color = status_rules[dado.status]["background"]
        text_color = status_rules[dado.status]["text"]
    # Se não for um dos status acima, verificar as condições baseadas em dias_diferenca
    elif dias_diferenca is not None:
        status_text = str(dado.novo_status)
        if 0 <= dias_diferenca <= 7:
            background_color = "#ffff00"  # Amarelo
            text_color = "#000000"        # Preto
        elif dias_diferenca < 0:
            background_color = "#ff0000"  # Vermelho
            text_color = "#FFFFFF"        # Branco
        elif dias_diferenca > 7:
            background_color = "#14a0b6"  # Ciano
            text_color = "#FFFFFF"        # Branco

    # Calcular a largura do fundo colorido, se houver status
    if status_text:
        status_width = p.stringWidth(status_text, 'Helvetica-Bold', 10) + 10  # Largura do fundo (com margem)

    # Desenhar o fundo colorido para o status, se aplicável
    if background_color and status_width:
        p.setFillColor(HexColor(background_color))
        p.rect(status_x, y - 2, status_width, status_height, fill=1, stroke=0)

    # Desenhar o texto completo do status
    p.setFillColor(HexColor("#000000"))  # Cor padrão do texto (preto)
    p.drawString(x, y, description_part)  # Parte inicial do texto (sem cor especial)

    # Desenhar o texto do status com a cor apropriada
    if status_text:
        p.setFillColor(HexColor(text_color if text_color else "#000000"))  # Cor do texto do status
        p.drawString(status_x + 5, y, status_text)  # Status com cor específica

    # Restaurar a cor de preenchimento para preto
    p.setFillColor(HexColor("#000000"))

    # Ajustar a posição y para os dados adicionais
    y -= 20

    # Adicionar os parágrafos iniciais com informações adicionais
    p.setFont("Helvetica", 10)
    p.drawString(x, y, f'Data de Início: {dado.DataDeInicio.strftime("%d/%m/%Y %H:%M") if dado.DataDeInicio else "-"}')
    y -= 20

    p.drawString(x, y, f'Data de Conclusão: {dado.DataDeConclusao.strftime("%d/%m/%Y %H:%M") if dado.DataDeConclusao else "Não concluído"}')
    y -= 20

    p.drawString(x, y, f"Área atendida: {dado.Areas}")
    y -= 20

    p.drawString(x, y, f"Tamanho da área atendida: {dado.Areas.dimensao if dado.Areas else "-"} M²")
    y -= 20

    p.drawString(x, y, "Serviços Escalados:")
    y -= 10
    servicos = formatar_atributos(queryset=dado.ServicosEscalados.all(), atributo='nome')
    p.drawString(x + 20, y, f"- {servicos}")
    y -= 20

    if permission_type == "jardinagem":
        p.drawString(x, y, "Colaboradores Escalados:")
        y -= 10
        colaborador = formatar_atributos(queryset=dado.ColaboradoresEscalados.all(), atributo='username')
        p.drawString(x + 20, y, f"- {colaborador}")
        y -= 20

    return y


def draw_checklist_table(p, x, y, width, height, dado, model, header_image_path):
    """
    Desenha uma tabela de checklist no PDF com base no modelo fornecido.

    Args:
        p: Objeto canvas do ReportLab (para desenhar no PDF).
        x: Posição x inicial da tabela.
        y: Posição y inicial da tabela.
        width: Largura total da página.
        height: Altura total da página.
        dado: Objeto contendo informações do agendamento (como id_random e DescricaoDoServico).
        model: Modelo do checklist (ex.: CheckListJardinagem ou CheckListLimpezaPredial).
        header_image_path: Caminho da imagem do cabeçalho para novas páginas.

    Returns:
        y: Nova posição y após desenhar a tabela.
    """
    # Filtrar os dados do checklist com base no modelo fornecido
    dados_checklist = carregar_checklists(dado, model)
    if not dados_checklist:
        return y  # Retorna a posição y sem alterações se não houver dados

    # Verificar se há espaço suficiente na página
    if y < 150:
        draw_footer(p, width)
        p.showPage()
        draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
        y = height - 120

    # Título da tabela
    p.setFont('Helvetica-Bold', 10)
    p.drawString(x, y, "Dados do Checklist:")
    y -= 15

    # Configurações da tabela
    col_widths = [90, 120, 120, 130, 80]  # Larguras das colunas
    headers = ["Agendamento.Id", "Agendamento.Descrição", "Checklist.Descrição",
               "Checklist.AtualizadoEm", "Checklist.Status"]
    row_height = 15

    # Desenhar cabeçalho da tabela
    p.setFillColorRGB(0.9, 0.9, 0.9)  # Cinza claro para o fundo do cabeçalho
    p.rect(x, y - row_height, sum(col_widths), row_height, fill=1)
    p.setFillColorRGB(0, 0, 0)  # Preto para o texto
    p.setFont("Helvetica-Bold", 9)
    for i, header in enumerate(headers):
        p.drawString(x + sum(col_widths[:i]) + 5, y - row_height + 3, header)
    y -= row_height

    # Desenhar linhas da tabela
    p.setFont("Helvetica", 9)
    for i, checklist in enumerate(dados_checklist):
        if y < 50:  # Verificar se precisa de nova página
            draw_footer(p, width)
            p.showPage()
            draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
            y = height - 120
            p.setFont("Helvetica", 9)

        # Alternar cores de fundo para linhas (branco e cinza claro)
        if i % 2 == 0:
            p.setFillColorRGB(1, 1, 1)  # Branco
        else:
            p.setFillColorRGB(0.95, 0.95, 0.95)  # Cinza muito claro
        p.rect(x, y - row_height, sum(col_widths), row_height, fill=1)
        p.setFillColorRGB(0, 0, 0)  # Preto para o texto

        # Preencher as colunas da linha
        p.drawString(x + 5, y - row_height + 3, str(checklist.servico_agendado.id))  # Agendamento.Id
        p.drawString(x + col_widths[0] + 5, y - row_height + 3,
                     str(dado.DescricaoDoServico))  # Agendamento.Descrição
        p.drawString(x + sum(col_widths[:2]) + 5, y - row_height + 3,
                     str(checklist.descricao))  # Checklist.Descrição
        p.drawString(x + sum(col_widths[:3]) + 5, y - row_height + 3,
                     checklist.atualizado_em.strftime("%d/%m/%Y %H:%M") if checklist.atualizado_em else "-")  # Checklist.AtualizadoEm

        # Configurar o status com fundo colorido
        status_text = str(checklist.status)
        status_x = x + sum(col_widths[:4]) + 5  # Posição inicial da coluna Status
        status_width = 70  # Largura do fundo colorido
        status_height = 10  # Altura do fundo colorido

        # Definir cor de fundo baseada no status
        if checklist.status == "Pendente":
            p.setFillColor(HexColor("#f6be04"))  # Amarelo
            p.rect(status_x, y - row_height + 2, status_width, status_height, fill=1, stroke=0)
        elif checklist.status == "Concluído":
            p.setFillColor(HexColor("#008000"))  # Verde
            p.rect(status_x, y - row_height + 2, status_width, status_height, fill=1, stroke=0)

        # Desenhar o texto do status
        p.setFillColorRGB(0, 0, 0)  # Preto para o texto
        p.drawString(status_x, y - row_height + 3, status_text)  # Checklist.Status

        y -= row_height

    # Espaço extra após a tabela
    y -= 20

    return y


def draw_execution_table(p, x, y, width, height, execucao_dados, header_image_path, page_number):
    """
    Desenha uma tabela de dados de execução no PDF.

    Args:
        p: Objeto canvas do ReportLab (para desenhar no PDF).
        x: Posição x inicial da tabela.
        y: Posição y inicial da tabela.
        width: Largura total da página.
        height: Altura total da página.
        execucao_dados: QuerySet contendo os dados de execução a serem exibidos.
        header_image_path: Caminho da imagem do cabeçalho para novas páginas.
        page_number: Número da página atual (passado como referência para controle).

    Returns:
        tuple: (y, page_number) - Nova posição y e número da página atualizado.
    """
    if not execucao_dados:
        return y, page_number  # Retorna sem alterações se não houver dados

    # Título da tabela
    p.setFont('Helvetica-Bold', 10)
    p.drawString(x, y, "Dados de Execução:")
    y -= 15

    # Configurações da tabela
    col_widths = [120, 120, 100, 100, 100]  # Larguras das colunas
    headers = ["Agendamento.Id", "Colaboradores.Nome", "DataHoraChegada",
               "DataHoraRetorno", "TempoEmAtividade"]
    row_height = 15

    # Desenhar cabeçalho da tabela
    p.setFillColorRGB(0.9, 0.9, 0.9)  # Cinza claro para o fundo
    p.rect(x, y - row_height, sum(col_widths), row_height, fill=1)
    p.setFillColorRGB(0, 0, 0)  # Preto para o texto
    p.setFont("Helvetica-Bold", 9)
    for i, header in enumerate(headers):
        p.drawString(x + sum(col_widths[:i]) + 6, y - row_height + 3, header)
    y -= row_height

    # Desenhar linhas da tabela
    p.setFont("Helvetica", 9)
    for i, execucao in enumerate(execucao_dados):
        if y < 50:  # Verificar se há espaço suficiente, senão criar nova página
            draw_footer(p, width)
            p.showPage()
            page_number += 1
            draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
            y = height - 120
            p.setFont("Helvetica", 9)

        # Alternar cores das linhas
        if i % 2 == 0:
            p.setFillColorRGB(1, 1, 1)  # Branco
        else:
            p.setFillColorRGB(0.95, 0.95, 0.95)  # Cinza muito claro
        p.rect(x, y - row_height, sum(col_widths), row_height, fill=1)
        p.setFillColorRGB(0, 0, 0)  # Preto para o texto

        # Escrever os dados nas colunas
        p.drawString(x + 5, y - row_height + 3, str(execucao.id_agendamento))  # Agendamento.Id
        p.drawString(x + col_widths[0] + 5, y - row_height + 3, str(execucao.colaboradores_chamados))  # Colaboradores.Nome
        p.drawString(x + sum(col_widths[:2]) + 5, y - row_height + 3,
                     execucao.data_hora_chegada.strftime("%d/%m/%Y %H:%M") if execucao.data_hora_chegada else "-")  # DataHoraChegada
        p.drawString(x + sum(col_widths[:3]) + 5, y - row_height + 3,
                     execucao.data_hora_retorno.strftime("%d/%m/%Y %H:%M") if execucao.data_hora_retorno else "-")  # DataHoraRetorno
        p.drawString(x + sum(col_widths[:4]) + 5, y - row_height + 3,
                     str(execucao.tempo_na_area) if execucao.tempo_na_area else "-")  # TempoEmAtividade
        y -= row_height

    # Espaço extra após a tabela
    y -= 20

    return y, page_number


def draw_request_and_delivery_images(p, x, y, width, height, dado, header_image_path, permission_type=None):
    """
    Desenha as imagens de solicitação e entrega no PDF, duas por página.

    Args:
        p: Objeto canvas do ReportLab.
        x: Posição x inicial.
        y: Posição y inicial.
        width: Largura total da página.
        height: Altura total da página.
        dado: Objeto contendo foto_solicitacao e foto_entrega.
        header_image_path: Caminho da imagem do cabeçalho para novas páginas.

    Returns:
        y: Nova posição y após desenhar as imagens.
    """
    images = []

    if permission_type == "jardinagem":
        # Adiciona a imagem da solicitação
        if dado.foto_solicitacao:
            images.append(("Na solicitação", dado.foto_solicitacao))
        else:
            images.append(("Na solicitação", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')))

    # Adiciona a imagem da entrega
    if dado.foto_entrega:
        images.append(("Na entrega", dado.foto_entrega))
    else:
        images.append(("Na entrega", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png')))

    # Processa as imagens duas por página
    for i in range(0, len(images), 2):
        if i > 0 or y < 400:  # Nova página após a primeira ou se não houver espaço
            draw_footer(p, width)
            p.showPage()
            draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
            y = height - 120

        # Primeira imagem da página
        title1, path1 = images[i]
        p.setFont("Helvetica", 10)
        p.drawString(x, y, title1)
        y -= 12
        height1 = draw_image(path1, x, y, p)
        y -= height1 + 10

        # Segunda imagem da página (se existir)
        if i + 1 < len(images):
            title2, path2 = images[i + 1]
            p.setFont("Helvetica", 10)
            p.drawString(x, y, title2)
            y -= 12
            height2 = draw_image(path2, x, y, p)
            y -= height2 + 10

    return y


def draw_all_images_intercalated(p, x, y, width, height, dado, header_image_path, checklist_model=None):
    """
    Desenha todas as imagens (solicitação, checklist e entrega) intercaladas no PDF, duas por página.

    Args:
        p: Objeto canvas do ReportLab.
        x: Posição x inicial.
        y: Posição y inicial.
        width: Largura total da página.
        height: Altura total da página.
        dado: Objeto contendo foto_solicitacao, foto_entrega e id_random.
        header_image_path: Caminho da imagem do cabeçalho para novas páginas.
        checklist_model: Modelo do checklist (padrão: CheckListJardinagem).

    Returns:
        y: Nova posição y após desenhar as imagens.
    """
    images = []

    # Adiciona a imagem da solicitação
    if dado.foto_solicitacao:
        images.append(("Na solicitação", dado.foto_solicitacao, False))
    else:
        images.append(("Na solicitação", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'), False))

    # Adiciona as imagens do checklist
    dados_checklist = carregar_checklists(dado, checklist_model)
    for checklist in dados_checklist:
        if checklist.foto_comprovacao:
            images.append((checklist.descricao, checklist.foto_comprovacao, True, checklist.status, checklist.atualizado_em))
        else:
            images.append((checklist.descricao, os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'),
                           True, checklist.status, checklist.atualizado_em))

    # Adiciona a imagem da entrega
    if dado.foto_entrega:
        images.append(("Na entrega", dado.foto_entrega, False))
    else:
        images.append(("Na entrega", os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'), False))

    # Processa as imagens duas por página
    for i in range(0, len(images), 2):
        if i > 0 or y < 400:  # Nova página após a primeira ou se não houver espaço
            draw_footer(p, width)
            p.showPage()
            draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
            y = height - 120

        # Primeira imagem da página
        title1, path1, is_checklist1 = images[i][0], images[i][1], images[i][2]
        status1 = images[i][3] if is_checklist1 else None
        atualizado_em1 = images[i][4] if is_checklist1 else None

        if is_checklist1:
            p.setFont("Helvetica", 8)
            p.drawString(x + 40, y, f"Descrição: {title1}")
            y -= 12
            p.setFont("Helvetica-Bold", 8)
            status_text = f"Status: {status1}"
            if status1 == "Pendente":
                p.setFillColor(HexColor("#f6be04"))
                p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
            elif status1 == "Concluído":
                p.setFillColor(HexColor("#008000"))
                p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
            p.setFillColor(HexColor("#000000"))
            p.drawString(x + 40, y, status_text)
            y -= 12
            p.setFont("Helvetica", 8)
            p.drawString(x + 40, y, f"Atualizado em: {atualizado_em1.strftime('%d/%m/%Y %H:%M') if atualizado_em1 else '-'}")
            y -= 12
            height1 = draw_image(path1, x + 40, y, p)
        else:
            p.setFont("Helvetica", 10)
            p.drawString(x, y, title1)
            y -= 12
            height1 = draw_image(path1, x, y, p)
        y -= height1 + 10

        # Segunda imagem da página (se existir)
        if i + 1 < len(images):
            title2, path2, is_checklist2 = images[i + 1][0], images[i + 1][1], images[i + 1][2]
            status2 = images[i + 1][3] if is_checklist2 else None
            atualizado_em2 = images[i + 1][4] if is_checklist2 else None

            if is_checklist2:
                p.setFont("Helvetica", 8)
                p.drawString(x + 40, y, f"Descrição: {title2}")
                y -= 12
                p.setFont("Helvetica-Bold", 8)
                status_text = f"Status: {status2}"
                if status2 == "Pendente":
                    p.setFillColor(HexColor("#f6be04"))
                    p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
                elif status2 == "Concluído":
                    p.setFillColor(HexColor("#008000"))
                    p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
                p.setFillColor(HexColor("#000000"))
                p.drawString(x + 40, y, status_text)
                y -= 12
                p.setFont("Helvetica", 8)
                p.drawString(x + 40, y, f"Atualizado em: {atualizado_em2.strftime('%d/%m/%Y %H:%M') if atualizado_em2 else '-'}")
                y -= 12
                height2 = draw_image(path2, x + 40, y, p)
            else:
                p.setFont("Helvetica", 10)
                p.drawString(x, y, title2)
                y -= 12
                height2 = draw_image(path2, x, y, p)
            y -= height2 + 10

    return y


def draw_checklist_images(p, x, y, width, height, dado, header_image_path, checklist_model=None):
    """
    Desenha as imagens do checklist no PDF, duas por página.

    Args:
        p: Objeto canvas do ReportLab.
        x: Posição x inicial.
        y: Posição y inicial.
        width: Largura total da página.
        height: Altura total da página.
        dado: Objeto contendo id_random para filtrar o checklist.
        header_image_path: Caminho da imagem do cabeçalho para novas páginas.
        checklist_model: Modelo do checklist (padrão: CheckListJardinagem).

    Returns:
        y: Nova posição y após desenhar as imagens.
    """
    images = []

    # Adiciona as imagens do checklist
    dados_checklist = carregar_checklists(dado, checklist_model)
    for checklist in dados_checklist:
        if checklist.foto_comprovacao:
            images.append((checklist.descricao, checklist.foto_comprovacao, checklist.status, checklist.atualizado_em))
        else:
            images.append((checklist.descricao, os.path.join(settings.STATICFILES_DIRS[0], 'dist/img/not found.png'),
                           checklist.status, checklist.atualizado_em))

    # Processa as imagens duas por página
    for i in range(0, len(images), 2):
        if i > 0 or y < 400:  # Nova página após a primeira ou se não houver espaço
            draw_footer(p, width)
            p.showPage()
            draw_header(c=p, header_image_path=header_image_path, width=width, height=height)
            y = height - 120

        # Primeira imagem da página
        title1, path1, status1, atualizado_em1 = images[i]
        p.setFont("Helvetica", 8)
        p.drawString(x + 40, y, f"Descrição: {title1}")
        y -= 12
        p.setFont("Helvetica-Bold", 8)
        status_text = f"Status: {status1}"
        if status1 == "Pendente":
            p.setFillColor(HexColor("#f6be04"))
            p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
        elif status1 == "Concluído":
            p.setFillColor(HexColor("#008000"))
            p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
        p.setFillColor(HexColor("#000000"))
        p.drawString(x + 40, y, status_text)
        y -= 12
        p.setFont("Helvetica", 8)
        p.drawString(x + 40, y, f"Atualizado em: {atualizado_em1.strftime('%d/%m/%Y %H:%M') if atualizado_em1 else '-'}")
        y -= 12
        height1 = draw_image(path1, x + 40, y, p)
        y -= height1 + 10

        # Segunda imagem da página (se existir)
        if i + 1 < len(images):
            title2, path2, status2, atualizado_em2 = images[i + 1]
            p.setFont("Helvetica", 8)
            p.drawString(x + 40, y, f"Descrição: {title2}")
            y -= 12
            p.setFont("Helvetica-Bold", 8)
            status_text = f"Status: {status2}"
            if status2 == "Pendente":
                p.setFillColor(HexColor("#f6be04"))
                p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
            elif status2 == "Concluído":
                p.setFillColor(HexColor("#008000"))
                p.rect(x + 40, y - 2, 100, 10, fill=1, stroke=0)
            p.setFillColor(HexColor("#000000"))
            p.drawString(x + 40, y, status_text)
            y -= 12
            p.setFont("Helvetica", 8)
            p.drawString(x + 40, y, f"Atualizado em: {atualizado_em2.strftime('%d/%m/%Y %H:%M') if atualizado_em2 else '-'}")
            y -= 12
            height2 = draw_image(path2, x + 40, y, p)
            y -= height2 + 10

    return y