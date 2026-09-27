from unidade.models import Unidade
from django import forms
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas
from empresaprimaria.models import EmpresaPrimaria
from zeladorx.models import TypeZeladoria

class UnidadeForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(UnidadeForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']
        setores = empresas['setores']

        if userid and type=='creat/edit':
            # Ajustar o queryset do campo 'empresaprimaria'
            # self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
            #     empresaprimaria__id_random__in=empresas_primarias_ids,
            #     id_random__in=empresas_secundarias_ids,
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['empresasecundaria'] = forms.ModelMultipleChoiceField(
                queryset=EmpresaSecundaria.objects.filter(
                    empresaprimaria__id_random__in=empresas_primarias_ids,
                    id_random__in=empresas_secundarias_ids,
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.CheckboxSelectMultiple(
                    attrs={
                        'class': 'checkboxl',
                    }
                ),
                label='Empresa operadora',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # self.fields['empresasecundaria'] = forms.ModelMultipleChoiceField(
            #     queryset=EmpresaSecundaria.objects.filter(
            #         empresaprimaria__id_random__in=empresas_primarias_ids,
            #     ).distinct(),
            #     widget=forms.SelectMultiple(
            #         attrs={
            #             'class': 'form-control',  # Modifique a classe se necessário
            #             'style': 'max-height: 40px; overflow-y: auto;'
            #         }
            #     ),
            #     label='Empresas que atende',
            #     required=False,
            #     initial=None
            # )

            self.fields['empresasecundaria'] = forms.ModelChoiceField(
                queryset=EmpresaSecundaria.objects.filter(
                    empresaprimaria__id_random__in=empresas_primarias_ids,
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 350px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Empresa operadora',
                required=False,  # ou False, conforme sua lógica
                initial=None
            )


        # Habilitar os campos se as condições forem verdadeiras
        if setores['habilitar_jardinagem_secundaria'] and setores['habilitar_jardinagem']:
            self.fields['linkmapajardinagem'].widget = forms.TextInput(
                attrs={'class': 'form-control'}
            )
        else:
            self.fields.pop('linkmapajardinagem')

        if setores['habilitar_limpeza_secundaria'] and setores['habilitar_limpeza']:
            self.fields['linkmapalimnpezapredial'].widget = forms.TextInput(
                attrs={'class': 'form-control'}
            )
        else:
            self.fields.pop('linkmapalimnpezapredial')

    empresasecundaria = forms.ModelMultipleChoiceField(
        queryset=EmpresaSecundaria.objects.all().distinct(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Empresa operadora',
        required=True  # Defina como True se a seleção de colaboradores for obrigató
    )

    class Meta:
        model = Unidade
        fields = ['nome', 'linkmapajardinagem', 'linkmapalimnpezapredial', 'empresasecundaria']
        labels = {
            'nome': 'Nome',
            'linkmapajardinagem': 'Link do mapa jardinagem da unidade',
            'linkmapalimnpezapredial': 'Link do mapa limpeza predial da unidade',
            'EmpresaSecundaria': 'Empresa operadora',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }