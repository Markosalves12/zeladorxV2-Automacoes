from django import forms
from areas.models_jardinagem import AreasJardins
from empresasecundario.utils import define_empresas
from terrenos.models import Terreno
from vegetacao.models import CatalogoVegetacao
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from localidade.models_Jardinagem import LocalidadeJardiangem

class AreasJardinsForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', **kwargs):
        super(AreasJardinsForms, self).__init__(*args, **kwargs)
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
                queryset=LocalidadeJardiangem.objects.filter(
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
                queryset=CatalogodeServicoJardinagem.objects.filter(
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

            # self.fields['vegetacao'].queryset = self.fields['vegetacao'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            #     EmpresaSecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['vegetacao'] = forms.ModelChoiceField(
                queryset=CatalogoVegetacao.objects.filter(
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
                label='Vegetação predominante',
                required=True  # ou False, conforme sua lógica
            )

            # self.fields['Terreno'].queryset = self.fields['Terreno'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            #     EmpresaSecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['Terreno'] = forms.ModelChoiceField(
                queryset=Terreno.objects.filter(
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
                label='Terreno predominante',
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
                queryset=LocalidadeJardiangem.objects.filter(
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
                queryset=CatalogodeServicoJardinagem.objects.filter(
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

            # self.fields['vegetacao'].queryset = self.fields['vegetacao'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['vegetacao'] = forms.ModelChoiceField(
                queryset=CatalogoVegetacao.objects.filter(
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
                label='Vegetação predominante',
                required=True  # ou False, conforme sua lógica
            )

            # self.fields['Terreno'].queryset = self.fields['Terreno'].queryset.filter(
            #     EmpresaSecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     EmpresaSecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()


            self.fields['Terreno'] = forms.ModelChoiceField(
                queryset=Terreno.objects.filter(
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
                label='Terreno predominante',
                required=True  # ou False, conforme sua lógica
            )

    class Meta:
        model = AreasJardins
        fields = ['nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'foto', 'periodicidade']

        labels = {
            'nome': 'Nome da região',
            'dimensao': 'Dimensão da área em M²',
            'vegetacao': 'Vegetação predominante',
            'Terreno': 'Terreno predominante',
            'servico': 'Serviço principal aplicado',
            'localidade': 'Localidade',
            'foto': 'Foto da região',
            'periodicidade': 'Periodicidade de retorno'
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
            'foto': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'periodicidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
