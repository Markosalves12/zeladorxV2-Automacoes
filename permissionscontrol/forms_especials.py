from django import forms
from permissionscontrol.models import PermissionsAccessEspecials, PermissionsEspecials
from empresasecundario.utils import define_empresas
from gerente.models import Gerente

class PermissionsAccessEspecialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(PermissionsAccessEspecialForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid:
            # self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            #     empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     empresasecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['Gerente'] = forms.ModelChoiceField(
                queryset=Gerente.objects.filter(
                    empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    empresasecundaria__id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Gerente',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            #     empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     empresasecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['Gerente'] = forms.ModelChoiceField(
                queryset=Gerente.objects.filter(
                    empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    empresasecundaria__id_random__in=empresas_secundarias_ids,
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
                label='Gerente',
                required=False  # ou False, conforme sua lógica
            )

            # Alterando o widget dos campos de seleção múltipla para SelectMultiple
            self.fields['Permissions'] = forms.ModelMultipleChoiceField(
                queryset=PermissionsEspecials.objects.distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 350px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Permissões concedidas',
                required=False,
            )

    Permissions = forms.ModelMultipleChoiceField(
        queryset=PermissionsEspecials.objects.distinct().order_by('Permissions'),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Permissões concedidas',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    class Meta:
        model = PermissionsAccessEspecials

        fields = ['Gerente', 'Permissions']

        labels = {
            'Gerente': 'Gerente',
            'Permissions': 'Permissões concedidas',
        }

        widgets = {
            # 'Gerente': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # ),
        }