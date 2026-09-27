from django.urls import path

from relatorios.limpeza_predial.views_relatorios_limpeza_predial_xlsx import (
    relatorios_de_servicos_limpeza_predial_xlsx_agendados,
    relatorios_de_servicos_limpeza_predial_xlsx_concluidos
)

from relatorios.limpeza_predial.views_relatorios_limpeza_predial_pdf import (
    relatorios_de_servicos_limpeza_predial_pdf_concluidos,
    relatorios_de_servicos_limpeza_predial_pdf_agendados
)

from relatorios.limpeza_predial.relatorio_de_servicos_limpeza_predial_xlsx import (
    exportar_relatorio_de_serivos_limpeza_predial_excel)

from relatorios.limpeza_predial.relatorio_de_servicos_limpeza_predial_pdf import (
    exportar_relatorio_de_serivos_limpeza_predial_pdf
)

from relatorios.limpeza_predial.relatorio_de_servicos_na_area_limpeza_predial_pdf import (
    exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf
)

from relatorios.limpeza_predial.relatorio_de_servicos_na_area_limpeza_predial_xlsx import (
    exportar_relatorio_de_serivos_na_area_limpeza_predial_excel)

from relatorios.limpeza_predial.relatorio_de_servicos_limpeza_predial_pdf_with_checklist import (
    exportar_relatorio_de_serivos_limpeza_predial_pdf_with_checklist)

from relatorios.limpeza_predial.relatorio_de_servicos_na_area_limpeza_predial_pdf_with_checklist import (
    exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf_with_checklist)

from relatorios.limpeza_predial.relatorio_de_servicos_limpeza_predial_xlsx_with_checklist import (
    exportar_relatorio_de_serivos_limpeza_predial_excel_with_checklist)

from relatorios.limpeza_predial.relatorio_de_servicos_na_area_limpeza_predial_xlsx_with_checklist import (
    exportar_relatorio_de_serivos_na_area_limpeza_predial_excel_with_checklist)

urlpatterns = [
    path(
        'relatorios-de-servicos-limpeza-predial-xlsx-concluidos/<str:userid>',
        relatorios_de_servicos_limpeza_predial_xlsx_concluidos,
        name='relatorios_de_servicos_limpeza_predial_xlsx_concluidos'
    ),
    path(
        'relatorios-de-servicos-limpeza-predial-xlsx-agendados/<str:userid>',
        relatorios_de_servicos_limpeza_predial_xlsx_agendados,
        name='relatorios_de_servicos_limpeza_predial_xlsx_agendados'
    ),
    path(
        'exportar-relatorio-de-serivos-limpeza-predial-excel/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_limpeza_predial_excel,
        name='exportar_relatorio_de_serivos_limpeza_predial_excel'
    ),
    path(
        'exportar-relatorio-de-serivos-limpeza-predial-pdf/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_limpeza_predial_pdf,
        name='exportar_relatorio_de_serivos_limpeza_predial_pdf'
    ),
    path(
        'relatorios-de-servicos-limpeza-predial-pdf-concluidos/<str:userid>',
        relatorios_de_servicos_limpeza_predial_pdf_concluidos,
        name='relatorios_de_servicos_limpeza_predial_pdf_concluidos'
    ),
    path(
        'relatorios-de-servicos-limpeza-predial-pdf-agendados/<str:userid>',
        relatorios_de_servicos_limpeza_predial_pdf_agendados,
        name='relatorios_de_servicos_limpeza_predial_pdf_agendados'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-limpeza-predial-pdf/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf,
        name='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-limpeza-predial-excel/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_limpeza_predial_excel,
        name='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel'
    ),
    path(
        'exportar-relatorio-de-serivos-Limpeza-predial-pdf-with-checklist/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_limpeza_predial_pdf_with_checklist,
        name='exportar_relatorio_de_serivos_limpeza_predial_pdf_with_checklist'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-Limpeza-predialpdf-with-checklist/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf_with_checklist,
        name='exportar_relatorio_de_serivos_na_area_limpeza_predial_pdf_with_checklist'
    ),
    path(
        'exportar-relatorio-de-serivos-Limpeza-predial-excel-with-checklist/<str:userid>/<str:status>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>',
        exportar_relatorio_de_serivos_limpeza_predial_excel_with_checklist,
        name='exportar_relatorio_de_serivos_limpeza_predial_excel_with_checklist'
    ),
    path(
        'exportar-relatorio-de-serivos-na-area-Limpeza-predial-excel-with-checklist/<str:userid>/<str:id_random>/<str:DataDeInicio>/'
        '<str:DataDeConclusao>/<str:Areas>/<str:TipoServico>/<str:ServicosEscalados>/<str:ColaboradoresEscalados>/'
        '<str:type>',
        exportar_relatorio_de_serivos_na_area_limpeza_predial_excel_with_checklist,
        name='exportar_relatorio_de_serivos_na_area_limpeza_predial_excel_with_checklist'
    ),
]
