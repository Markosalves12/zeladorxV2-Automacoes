from typing import Optional, List, Dict, Any

def define_filters(
        DataDeInicio: Optional[str] = None,
        DataDeConclusao: Optional[str] = None,
        TipoServico: Optional[str] = None,
        Areas: Optional[str] = None,
        ServicosEscalados: Optional[List[str]] = None,
        ColaboradoresEscalados: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Constrói um dicionário de filtros para consultas com base nos parâmetros fornecidos.

    Args:
        DataDeInicio: Data inicial para filtro (>=)
        DataDeConclusao: Data de conclusão para filtro (<=)
        TipoServico: Tipo de serviço para filtro exato
        Areas: ID da área para filtro exato
        ServicosEscalados: Lista de IDs de serviços escalados para filtro 'in'
        ColaboradoresEscalados: Lista de IDs de colaboradores escalados para filtro 'in'

    Returns:
        Dicionário com os filtros aplicáveis
    """
    filters = dict()

    if DataDeInicio and DataDeInicio != "None":
        filters['DataDeInicio__gte'] = DataDeInicio

    if DataDeConclusao and DataDeConclusao != "None":
        filters['DataDeConclusao__lte'] = DataDeConclusao

    if TipoServico and TipoServico != "None":
        filters['TipoServico'] = TipoServico

    if Areas and Areas != "None":
        filters['Areas__id'] = Areas

    if ServicosEscalados and ServicosEscalados != ["None"]:
        filters['ServicosEscalados__id__in'] = ServicosEscalados

    if ColaboradoresEscalados and ColaboradoresEscalados != ["None"]:
        filters['ColaboradoresEscalados__id__in'] = ColaboradoresEscalados

    return filters