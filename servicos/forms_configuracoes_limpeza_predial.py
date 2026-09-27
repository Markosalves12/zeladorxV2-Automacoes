from django import forms
from servicos.models_limpeza_predial import ServicoLimpezaPredialConfigurado
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from semana.models import DiasDaSemana
from empresasecundario.utils import define_empresas
from areas.models_limpeza_predial import AreaLimpezaPredial


class ServicoLimpezaPredialConfiguradoForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(ServicoLimpezaPredialConfiguradoForms, self).__init__(*args, **kwargs)
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
                queryset=CatalogodeServicoLimpezaPredial.objects.filter(
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

            # self.fields['Areas'].queryset = self.fields['Areas'].queryset.filter(
            #     localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            #     localidade__unidade__empresasecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado'],
            #     localidade__status__in=['Mobilizado'],
            #     localidade__unidade__status__in=['Mobilizado']
            # ).distinct()

            self.fields['Areas'] = forms.ModelChoiceField(
                queryset=AreaLimpezaPredial.objects.filter(
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
                label='Área',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # self.fields['ServicosEscalados'].queryset = self.fields['ServicosEscalados'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['ServicosEscalados'] = forms.ModelMultipleChoiceField(
                queryset=CatalogodeServicoLimpezaPredial.objects.filter(
                    EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 350px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Serviços Escalados',
                required=False,
                initial=None
            )

            # self.fields['Areas'].queryset = self.fields['Areas'].queryset.filter(
            #     localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['Areas'] = forms.ModelChoiceField(
                queryset=AreaLimpezaPredial.objects.filter(
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
                label='Área',
                required=False  # ou False, conforme sua lógica
            )

            self.fields['diasaseremrealizado'] = forms.ModelMultipleChoiceField(
                queryset=DiasDaSemana.objects.distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': 'max-height: 40px; overflow-y: auto;'
                    }
                ),
                label='Dias a serem realizados',
                required=False,
                initial=None
            )

    ServicosEscalados = forms.ModelMultipleChoiceField(
        queryset=CatalogodeServicoLimpezaPredial.objects.distinct(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Serviços escalados',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    diasaseremrealizado = forms.ModelMultipleChoiceField(
        queryset=DiasDaSemana.objects.distinct(),  # Usa as opções definidas no modelo
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Dias a serem realizados',
        required=True  # Defina como True se a seleção de dias for obrigatória
    )

    class Meta:
        model = ServicoLimpezaPredialConfigurado
        fields = ['Areas', 'ServicosEscalados', 'tempomedioplanejado', 'diasaseremrealizado','horario_1',
                  'horario_2', 'horario_3', 'horario_4', 'horario_5',
                  'horario_6', 'horario_7'
        ]

        labels = {
            'Areas': 'Área',
            'ServicosEscalados': 'Serviços Escalados',
            'TipoServico': 'Tipo de agendamento',
            'tempomedioplanejado': 'Tempo médio planejado',
            'diasaseremrealizado': 'Dias a serem realizados',
            'horario_1': 'Horario 1',
            'horario_2': 'Horario 2',
            'horario_3': 'Horario 3',
            'horario_4': 'Horario 4',
            'horario_5': 'Horario 5',
            'horario_6': 'Horario 6',
            'horario_7': 'Horario 7',
        }

        widgets = {
            'Areas': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'tempomedioplanejado': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_1': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_2': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_3': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_4': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_5': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_6': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),

            'horario_7': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'HH:MM'
                }
            ),
        }