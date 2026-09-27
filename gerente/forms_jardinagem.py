from django import forms
from gerente.models import Gerente
from empresasecundario.models import EmpresaSecundaria
from empresasecundario.utils import define_empresas
from empresasecundario.models import EmpresaSecundaria

class GerenteJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type = 'creat/edit', **kwargs):
        super(GerenteJardinagemForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        is_super_user = Gerente.objects.get(id_random=userid).is_superuser

        if userid and type=='creat/edit':
            # self.fields['empresasecundaria'].queryset = self.fields['empresasecundaria'].queryset.filter(
            #     empresaprimaria__id_random__in=empresas_primarias_ids,
            #     setor__setor='Jardinagem',
            #     status__in=['Mobilizado']
            # ).distinct()

            self.fields['empresasecundaria'] = forms.ModelMultipleChoiceField(
                queryset=EmpresaSecundaria.objects.filter(
                    empresaprimaria__id_random__in=empresas_primarias_ids,
                    setor__setor='Jardinagem',
                    status__in=['Mobilizado']
                ).distinct(),
                widget=forms.CheckboxSelectMultiple(
                    attrs={
                        'class': 'checkbox'
                    }
                ),
                label='Empresa Secundaria',
                required=True  # ou False, conforme sua lógica
            )

        if is_super_user:
            self.fields['is_superuser'] = forms.BooleanField(
                required=False,
                widget=forms.CheckboxInput(
                    attrs={
                        'class': 'checkbox'
                    }
                )
            )
        else:
            # Remove o campo 'is_superuser' se o usuário não for is_superuser
            self.fields.pop('is_superuser', None)

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            self.fields['empresasecundaria'] = forms.ModelMultipleChoiceField(
                queryset=EmpresaSecundaria.objects.filter(
                    empresaprimaria__id_random__in=empresas_primarias_ids,
                    setor__setor='Jardinagem',
                ).distinct(),
                widget=forms.SelectMultiple(
                    attrs={
                        'class': 'form-control',  # Modifique a classe se necessário
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 400px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Empresa Secundaria',
                required=False,
                initial=None
            )

    empresasecundaria = forms.ModelMultipleChoiceField(
        queryset=EmpresaSecundaria.objects.distinct(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Empresas que atende',
        required=True  # Defina como True se a seleção de colaboradores for obrigató
    )

    class Meta:
        model = Gerente
        fields = ['username', 'email', 'empresasecundaria', 'is_superuser', ]
        labels = {
            'username': 'Nome do gerente',
            'email': 'Email de contato',
            'empresasecundaria': 'Empresa Secundaria',
            'is_superuser': 'É super usuário'
        }

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'checkbox'
                }
            ),
        }