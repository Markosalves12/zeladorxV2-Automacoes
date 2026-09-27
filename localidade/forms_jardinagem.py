from django import forms
from localidade.models_Jardinagem import LocalidadeJardiangem
from empresasecundario.utils import define_empresas
from unidade.models import Unidade

class LocalidadeJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(LocalidadeJardinagemForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            # self.fields['unidade'].queryset = self.fields['unidade'].queryset.filter(
            #     empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     empresasecundaria__id_random__in=empresas_secundarias_ids,
            #     empresasecundaria__status__in=['Mobilizado'],
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['unidade'] = forms.ModelChoiceField(
                queryset=Unidade.objects.filter(
                    empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    empresasecundaria__id_random__in=empresas_secundarias_ids,
                    empresasecundaria__status__in=['Mobilizado'],
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Unidade',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # self.fields['unidade'].queryset = self.fields['unidade'].queryset.filter(
            #     empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     empresasecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['unidade'] = forms.ModelChoiceField(
                queryset=Unidade.objects.filter(
                    empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    empresasecundaria__id_random__in=empresas_secundarias_ids,
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
                label='Unidade',
                required=True  # ou False, conforme sua lógica
            )

    class Meta:
        model = LocalidadeJardiangem
        fields = ['nome', 'lat_med', 'long_med', 'unidade', ]
        labels = {
            'nome': 'Localidade',
            'lat_med': 'Latitude média',
            'long_med': 'Longitude média',
            'unidade': 'Unidade'
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lat_med': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'long_med': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            # 'unidade': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # )
        }