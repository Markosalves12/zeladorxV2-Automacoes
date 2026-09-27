from servicos.models_jardinagem import ServicoJardinagemAgendado, FatoServicoJardinagem
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from gerente.models import Gerente
from django import forms
from empresasecundario.utils import define_empresas
from areas.models_jardinagem import AreasJardins

class ServicoJaridinagemAgendadoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(ServicoJaridinagemAgendadoForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            # self.fields['ServicosEscalados'].queryset = self.fields['ServicosEscalados'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            #     EmpresaSecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['ServicosEscalados'] = forms.ModelMultipleChoiceField(
                queryset=CatalogodeServicoJardinagem.objects.filter(
                    EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                    EmpresaSecundaria__status__in=['Mobilizado'],
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.CheckboxSelectMultiple(
                    attrs={
                        'class': 'checkbox'
                    }
                ),
                label='Serviços Escalados',
                required=True  # ou False, conforme sua lógica
            )

            self.fields['ColaboradoresEscalados'] = forms.ModelMultipleChoiceField(
                queryset=Gerente.objects.filter(
                    empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    empresasecundaria__id_random__in=empresas_secundarias_ids,
                    empresasecundaria__status__in=['Mobilizado'],
                    empresasecundaria__setor__setor__in=['Jardinagem'],
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.CheckboxSelectMultiple(
                    attrs={
                        'class': 'checkbox',  # Modifique a classe se necessário
                    }
                ),
                label='Colaboradores escalados',
                required=False,
            )


            self.fields['Areas'] = forms.ModelChoiceField(
                queryset=AreasJardins.objects.filter(
                    localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                    localidade__unidade__empresasecundaria__status__in=['Mobilizado'],
                    status__in=['Mobilizado'],
                    localidade__status__in=['Mobilizado'],
                    localidade__unidade__status__in=['Mobilizado']
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Área para ser atendida',
                required=True  # ou False, conforme sua lógica
            )

            all_choices = self.fields['TipoServico'].choices
            filtered_choices = [choice for choice in all_choices if choice[0] != 'Automático']
            self.fields['TipoServico'].choices = filtered_choices

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # Redefinindo o campo Areas com filtro e widget
            self.fields['Areas'] = forms.ModelChoiceField(
                queryset=AreasJardins.objects.filter(
                    localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 300px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Área para ser atendida',
                required=True  # ou False, conforme sua lógica
            )

            # Alterando o widget dos campos de seleção múltipla para SelectMultiple
            self.fields['ServicosEscalados'] = forms.ModelMultipleChoiceField(
                queryset=CatalogodeServicoJardinagem.objects.filter(
                    EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 300px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        ),
                    }
                ),
                label='Serviços escalados',
                required=False,
            )

            self.fields['ColaboradoresEscalados'] = forms.ModelMultipleChoiceField(
                queryset=Gerente.objects.filter(
                    empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    empresasecundaria__id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 300px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Colaboradores escalados',
                required=False,
            )

    ServicosEscalados = forms.ModelMultipleChoiceField(
        queryset=CatalogodeServicoJardinagem.objects.distinct(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Serviços escalados',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    ColaboradoresEscalados = forms.ModelMultipleChoiceField(
        queryset=Gerente.objects.distinct(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Colaboradores escalado',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    class Meta:
        model = ServicoJardinagemAgendado
        fields = ['Areas', 'TipoServico', 'DescricaoDoServico', 'ServicosEscalados', 'DataDeInicio', 'DataDeConclusao', 'ColaboradoresEscalados',
                  'foto_solicitacao', 'foto_entrega',]

        labels = {
            'Areas': 'Área para ser atendida',
            'TipoServico': 'Tipo de agendamento',
            'ServicosEscalados': 'Serviços Escalados',
            'DescricaoDoServico': 'Descrição do serviço',
            'DataDeInicio': 'Data marcada para inicio',
            'DataDeConclusao': 'Data prevista para conclusao',
            'ColaboradoresEscalados': 'Colaboradores escalados',
            'foto_solicitacao': 'Foto da área na solicitação',
            'foto_entrega': 'Foto da área na entrega',
        }

        widgets = {
            'DataDeInicio': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',  # <- formato exigido por input[type=datetime-local]
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DDTHH:MM',
                }
            ),
            'DataDeConclusao': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',  # <- formato exigido por input[type=datetime-local]
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DDTHH:MM',
                }
            ),
            'TipoServico': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'DescricaoDoServico': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto_solicitacao': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto_entrega': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class FatoServicoJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, id_random=str, **kwargs):
        super(FatoServicoJardinagemForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        self.fields['Servico'].queryset = self.fields['Servico'].queryset.filter(
            id_random=id_random
        ).distinct()

        self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            empresasecundaria__id_random__in=empresas_secundarias_ids,
            empresasecundaria__status__in=['Mobilizado'],
            empresasecundaria__setor__setor__in=['Jardinagem'],
            status__in=['Mobilizado']
        ).distinct()

    class Meta:
        model = FatoServicoJardinagem
        fields = ['Servico', 'data_hora_chegada_na_area', 'data_hora_retorno_area', 'Gerente']

        labels = {
            'Servico': 'Serviço agendado',
            'data_hora_chegada_na_area': 'Chegada na área',
            'data_hora_retorno_area': 'Retorno da área',
            'Gerente': 'Colaborador',
        }

        widgets = {
            'Servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'data_hora_chegada_na_area':forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',  # <- formato exigido por input[type=datetime-local]
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DDTHH:MM',
                }
            ),
            'data_hora_retorno_area': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',  # <- formato exigido por input[type=datetime-local]
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'YYYY-MM-DDTHH:MM',
                }
            ),
            'Gerente': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
