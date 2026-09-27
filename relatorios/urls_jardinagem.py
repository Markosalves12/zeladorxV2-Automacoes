from django.urls import path

from relatorios.jardinagem.views_relatorios_jardinagem_xlsx import (relatorios_de_servicos_jardinagem_xlsx_agendados,
                                                                    relatorios_de_servicos_jardinagem_xlsx_concluidos)

from relatorios.jardinagem.views_relatorios_jardinagem_pdf import (relatorios_de_servicos_jardinagem_pdf_concluidos,
                                                                   relatorios_de_servicos_jardinagem_pdf_agendados)

from relatorios.jardinagem.relatorio_de_servicos_jardinagem_xlsx import exportar_relatorio_de_serivos_Jardinagem_excel

from relatorios.jardinagem.relatorio_de_servicos_jardinagem_pdf import exportar_relatorio_de_serivos_Jardinagem_pdf

from relatorios.jardinagem.relatorio_de_servicos_na_area_jardinagem_pdf import (
    exportar_relatorio_de_serivos_na_area_jardinagem_pdf
)

from relatorios.jardinagem.relatorio_de_servicos_na_area_jardinagem_xlsx import (
    exportar_relatorio_de_serivos_na_area_Jardinagem_excel
)

from relatorios.jardinagem.relatorio_de_servicos_jardinagem_pdf_with_checklist import (
    exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist)

from relatorios.jardinagem.relatorio_de_servicos_na_area_jardinagem_pdf_with_checklist import (
    exportar_relatorio_de_serivos_na_area_jardinagem_pdf_with_checklist)

from relatorios.jardinagem.relatorio_de_servicos_jardinagem_xlsx_with_checklist import (
    exportar_relatorio_de_serivos_Jardinagem_excel_with_checklist)

from relatorios.jardinagem.relatorio_de_servicos_na_area_jardinagem_xlsx_with_checklist import (
    exportar_relatorio_de_serivos_na_area_Jardinagem_excel_with_checklist)

urlpatterns = [
    path(
        'relatorios-de-servicos-jardinagem-xlsx-concluidos/<str:userid>/',
        relatorios_de_servicos_jardinagem_xlsx_concluidos,
        name='relatorios_de_servicos_jardinagem_xlsx_concluidos'
    ),
    path(
        'relatorios-de-servicos-jardinagem-xlsx-agendados/<str:userid>',
        relatorios_de_servicos_jardinagem_xlsx_agendados,
        name='relatorios_de_servicos_jardinagem_xlsx_agendados'
    ),
    path(
        'exportar-relatorio-de-serivos-Jardinagem-excel/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_Jardinagem_excel,
        name='exportar_relatorio_de_serivos_Jardinagem_excel'
    ),
    path(
        'exportar-relatorio-de-serivos-Jardinagem-pdf/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_Jardinagem_pdf,
        name='exportar_relatorio_de_serivos_Jardinagem_pdf'
    ),
    path(
        'relatorios-de-servicos-jardinagem-pdf-concluidos/<str:userid>',
        relatorios_de_servicos_jardinagem_pdf_concluidos,
        name='relatorios_de_servicos_jardinagem_pdf_concluidos'
    ),
    path(
        'relatorios-de-servicos-jardinagem-pdf-agendados/<str:userid>',
        relatorios_de_servicos_jardinagem_pdf_agendados,
        name='relatorios_de_servicos_jardinagem_pdf_agendados'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-jardinagem-pdf/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_jardinagem_pdf,
        name='exportar_relatorio_de_serivos_na_area_jardinagem_pdf'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-Jardinagem-excel/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_Jardinagem_excel,
        name='exportar_relatorio_de_serivos_na_area_Jardinagem_excel'
    ),
    path(
        'exportar-relatorio-de-serivos-Jardinagem-pdf-with-checklist/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist,
        name='exportar_relatorio_de_serivos_Jardinagem_pdf_with_checklist'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-jardinagem-pdf-with-checklist/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_jardinagem_pdf_with_checklist,
        name='exportar_relatorio_de_serivos_na_area_jardinagem_pdf_with_checklist'
    ),
    path(
        'exportar-relatorio-de-serivos-Jardinagem-excel-with-checklist/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_Jardinagem_excel_with_checklist,
        name='exportar_relatorio_de_serivos_Jardinagem_excel_with_checklist'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-Jardinagem-excel-with-checklist/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_Jardinagem_excel_with_checklist,
        name='exportar_relatorio_de_serivos_na_area_Jardinagem_excel_with_checklist'
    ),
]
