import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.geometry import Polygon
from openpyxl import Workbook
from django.http import HttpResponse
from django.core.files.storage import default_storage
from io import BytesIO
from openpyxl.drawing.image import Image
from medidor.models import DocsFromProcess


def processar_poligonos(request, id_random):
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
                nome = rest[0].strip() if rest else ''
                descricao = ','.join(rest[1:]).strip() if len(rest) > 1 else ''

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

    # Cria o workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Dimensionamento"
    ws.append(list(df.columns))
    for row in df.itertuples(index=False):
        ws.append(row)

    # Processa gráficos para colunas relevantes
    for coluna in df.drop(columns=['WKT', 'nome', 'descrição'], errors='ignore').columns:
        df[coluna] = df[coluna].astype(str).str.strip().str.capitalize()
        valores_unicos = sorted(df[coluna].dropna().unique())

        if len(valores_unicos) <= 30:
            plt.figure(figsize=(10, 8))
            cores = plt.cm.get_cmap('tab20', len(valores_unicos))
            for valor, cor in zip(valores_unicos, cores.colors):
                subset = df[df[coluna] == valor]
                for wkt_str, nome in zip(subset['WKT'], subset.get('nome', [''] * len(subset))):
                    if pd.notna(wkt_str):
                        try:
                            polygon = wkt.loads(wkt_str)
                            if isinstance(polygon, Polygon):
                                x, y = polygon.exterior.xy
                                plt.fill(x, y, color=cor, alpha=0.5)
                                centroid = polygon.centroid
                                plt.text(centroid.x, centroid.y, nome, fontsize=5, ha='center')
                        except Exception:
                            continue
                plt.plot([], [], color=cor, label=f"{valor}")

            plt.legend(title=coluna)
            plt.title(f"Polígonos por {coluna}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")

            img_bytes = BytesIO()
            plt.savefig(img_bytes, format='png')
            plt.close()

            ws_img = wb.create_sheet(title=coluna)
            img_bytes.seek(0)
            ws_img.add_image(Image(img_bytes), 'A1')

    # Prepara a resposta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="poligonos_processados_{id_random}.xlsx"'
    wb.save(response)
    return response