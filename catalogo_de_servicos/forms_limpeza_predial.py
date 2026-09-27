from django import forms
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria

class CatalogoServicoLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid, type = 'creat/edit', **kwargs):
        super(CatalogoServicoLimpezaPredialForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            # self.fields['EmpresaSecundaria'].queryset = self.fields['EmpresaSecundaria'].queryset.filter(
            #     empresaprimaria__id_random__in=empresas_primarias_ids,
            #     id_random__in=empresas_secundarias_ids,
            #     setor__setor__in = ['Limpeza predial'],
            #     status__in=['Mobilizado']
            # )

            self.fields['EmpresaSecundaria'] = forms.ModelChoiceField(
                queryset=EmpresaSecundaria.objects.filter(
                    empresaprimaria__id_random__in=empresas_primarias_ids,
                    id_random__in=empresas_secundarias_ids,
                    setor__setor__in=['Limpeza predial'],
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Empresa prestadora',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['EmpresaSecundaria'] = forms.ModelChoiceField(
                queryset=EmpresaSecundaria.objects.filter(
                    empresaprimaria__id_random__in=empresas_primarias_ids,
                    id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 400px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Empresa prestadora',
                required=True  # ou False, conforme sua lógica
            )

    class Meta:
        model = CatalogodeServicoLimpezaPredial
        fields = ['nome', 'EmpresaSecundaria', ]

        labels = {
            'nome': 'Nome do serviço',
            'EmpresaSecundaria': 'Empresa prestadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            # 'EmpresaSecundaria': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # ),
        }
