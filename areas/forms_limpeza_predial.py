from django import forms
from areas.models_limpeza_predial import AreaLimpezaPredial
from empresasecundario.utils import define_empresas
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial

class AreasLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', **kwargs):
        super(AreasLimpezaPredialForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        # Ajustar o queryset do campo 'empresaprimaria'
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            # self.fields['localidade'].queryset = self.fields['localidade'].queryset.filter(
            #     unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            #     unidade__empresasecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado'],
            #     unidade__status__in=['Mobilizado'],
            # ).distinct()

            self.fields['localidade'] = forms.ModelChoiceField(
                queryset=LocalidadeLimpezaPredial.objects.filter(
                    unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                    unidade__empresasecundaria__status__in=['Mobilizado'],
                    status__in=['Mobilizado'],
                    unidade__status__in=['Mobilizado'],
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Localidade',
                required=True  # ou False, conforme sua lógica
            )

            # self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            #     EmpresaSecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['servico'] = forms.ModelChoiceField(
                queryset=CatalogodeServicoLimpezaPredial.objects.filter(
                    EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
                    EmpresaSecundaria__status__in=['Mobilizado'],
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Serviço principal aplicado',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # self.fields['localidade'].queryset = self.fields['localidade'].queryset.filter(
            #     unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['localidade'] = forms.ModelChoiceField(
                queryset=LocalidadeLimpezaPredial.objects.filter(
                    unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
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
                label='Localidade',
                required=True  # ou False, conforme sua lógica
            )

            # self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['servico'] = forms.ModelChoiceField(
                queryset=CatalogodeServicoLimpezaPredial.objects.filter(
                    EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
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
                label='Serviço principal aplicado',
                required=True  # ou False, conforme sua lógica
            )

    class Meta:
        model = AreaLimpezaPredial
        fields = ['nome', 'dimensao', 'servico', 'localidade', 'foto']

        labels = {
            'nome': 'Nome da região',
            'dimensao': 'Dimensão da área em M²',
            'servico': 'Serviço principal aplicado',
            'localidade': 'Localidade',
            'foto': 'Foto da região',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'dimensao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            # 'servico': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # ),
            # 'localidade': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # ),
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }



