from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import List, Tuple, Any, Optional


def criar_workbook_com_sheets(sheet_configs: List[Tuple[str, Optional[List[str]], Optional[List[Tuple[str, Optional[str]]]]]]) -> Workbook:
    """
    Cria um workbook com múltiplas sheets e opcionalmente adiciona cabeçalhos e dados.

    Args:
        sheet_configs: Lista de tuplas (nome_da_sheet, headers, colunas)
                      onde headers e colunas são opcionais (podem ser None)

    Returns:
        Workbook configurado
    """
    wb = Workbook()
    # Remove a sheet padrão criada automaticamente
    wb.remove(wb.active)

    for sheet_name, headers, colunas in sheet_configs:
        ws = wb.create_sheet(title=sheet_name)
        if headers:
            adicionar_cabecalhos(ws, headers)
        # Se houver dados para adicionar, você pode passar como parâmetro adicional

    return wb


def adicionar_cabecalhos(worksheet: Worksheet, headers: List[str], row: int = 1) -> None:
    """
    Adiciona cabeçalhos a uma planilha do Excel.

    Args:
        worksheet: Worksheet do openpyxl onde os cabeçalhos serão adicionados
        headers: Lista de strings com os títulos dos cabeçalhos
        row: Número da linha onde os cabeçalhos serão inseridos (padrão: 1)
    """
    for col_num, header_title in enumerate(headers, 1):
        cell = worksheet.cell(row=row, column=col_num)
        cell.value = header_title


def adicionar_dados(
    worksheet: Worksheet,
    dados: List[Any],
    colunas: List[Tuple[str, Optional[str]]],
    headers: List[str],
    start_row: int = 2,
    column_width: int = 25
) -> None:
    # Ajusta a largura das colunas
    for col in range(1, len(headers) + 1):
        column_letter = worksheet.cell(row=1, column=col).column_letter
        worksheet.column_dimensions[column_letter].width = column_width

    # Adiciona os dados
    for row_num, row in enumerate(dados, start=start_row):
        for col_num, (attr_name, attr_type) in enumerate(colunas, start=1):
            cell = worksheet.cell(row=row_num, column=col_num)
            value = None

            if attr_type == 'nested':
                # Para atributos aninhados como 'servico_agendado.id'
                parts = attr_name.split('.')
                value = row
                for part in parts:
                    if value is None:
                        break
                    # Verifica se o objeto tem o atributo, sem depender de Model
                    if hasattr(value, part):
                        value = getattr(value, part)
                    else:
                        value = None
                        break
            else:
                # Para atributos diretos
                value = getattr(row, attr_name, None)

            # Tratamento especial para tipos
            if value is not None:
                if attr_type == 'data':
                    value = value.replace(tzinfo=None) if value else None
                elif attr_type == 'datetime_str':
                    value = value.strftime("%d/%m/%Y %H:%M") if value else "N/A"
                elif attr_type == 'url':
                    value = value.url if value else "N/A"

            cell.value = value