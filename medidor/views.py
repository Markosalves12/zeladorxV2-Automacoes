import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.geometry import Polygon
from openpyxl import Workbook
from django.core.files.storage import default_storage
from io import BytesIO
import base64
from medidor.forms import UploadFileForm
from medidor.models import DocsFromProcess
from django.shortcuts import render


def processar_poligonos_preview(id_random):
    objeto = DocsFromProcess.objects.get(id_random=id_random)

    # Lê o arquivo do storage
    with default_storage.open(objeto.document.name, 'rb') as file:
        df = pd.read_csv(file) if objeto.document.name.endswith('.csv') else pd.read_excel(file)

    # Verifica se tem 'WKT' ou tenta identificar colunas misturadas
    if 'WKT' not in df.columns:
        # Assume que a primeira coluna contém dados misturados
        mixed_column = df.columns[0]

        # Função para extrair WKT, nome e descrição de uma string misturada
        def split_mixed_data(row):
            text = str(row).strip()
            try:
                # Encontra o WKT (assume que começa com POLYGON)
                wkt_start = text.find('POLYGON')
                if wkt_start == -1:
                    return pd.Series({'WKT': None, 'nome': None, 'descrição': None})

                wkt_end = text.find('))') + 2
                wkt_str = text[wkt_start:wkt_end]

                # O restante é nome e descrição
                rest = text[wkt_end + 1:].split(',')
                nome = rest[0].strip() if rest else 'Não identificado'
                descricao = ','.join(rest[1:]).strip() if len(rest) > 1 else 'Não identificado'

                return pd.Series({'WKT': wkt_str, 'nome': nome, 'descrição': descricao})
            except Exception:
                return pd.Series({'WKT': None, 'nome': None, 'descrição': None})

        # Aplica o split na coluna misturada
        df[['WKT', 'nome', 'descrição']] = df[mixed_column].apply(split_mixed_data)

        # Remove a coluna original misturada
        df = df.drop(columns=[mixed_column])

        # Verifica se conseguiu extrair WKT
        if df['WKT'].isna().all():
            raise ValueError("Não foi possível identificar dados WKT no arquivo.")

    # Calcula a área estimada
    df['Área estimada'] = df['WKT'].apply(
        lambda w: wkt.loads(w).area * 111319.9 ** 2 if pd.notna(w) and isinstance(wkt.loads(w), Polygon) else None)

    # Preenche valores nulos
    df.fillna('Não identificado', inplace=True)

    # Gerar gráfico de prévia
    plt.figure(figsize=(6, 4))
    for wkt_str in df['WKT'].dropna():
        if wkt_str != 'Não identificado':  # Ignora valores inválidos
            try:
                polygon = wkt.loads(wkt_str)
                if isinstance(polygon, Polygon):
                    x, y = polygon.exterior.xy
                    plt.plot(x, y, alpha=0.5)
            except Exception:
                continue
    plt.title("Prévia de Polígonos")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    # Gerar arquivo Excel em memória
    wb = Workbook()
    ws = wb.active
    ws.append(list(df.columns))
    for row in df.itertuples(index=False):
        ws.append(row)

    excel_bytes = BytesIO()
    wb.save(excel_bytes)
    excel_bytes.seek(0)

    # Retorna a tabela HTML (primeiras 10 linhas), imagem base64 e Excel em memória
    return df.head(10).to_html(classes='table table-striped'), img_base64, excel_bytes


def medidor_upload(request, userid):
    form = UploadFileForm()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            objeto = form.save(commit=False)
            objeto.save()

            tabela_html, img_base64, excel_bytes = processar_poligonos_preview(objeto.id_random)
            request.session['excel_file'] = base64.b64encode(excel_bytes.read()).decode('utf-8')

            return render(
                request,
                'DataTableAndForms/medidor.html',
                {
                    'form': form,
                    'app_name': 'Dimensionador',
                    'id_random': objeto.id_random,
                    'tabela_html': tabela_html,
                    'img_base64': img_base64,
                    'download_ready': True,
                }
            )

    return render(
        request,
        'DataTableAndForms/medidor.html',
        {
            'form': form,
            'app_name': 'Dimensionador',
            'download_ready': False,
        }
    )
