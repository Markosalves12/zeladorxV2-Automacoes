from django import forms
from checklists.models import CheckListJardinagem
from empresasecundario.utils import define_empresas
from servicos.models_jardinagem import ServicoJardinagemAgendado


class CheckListJardinagemForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', id_random=False, **kwargs):
        super(CheckListJardinagemForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        # Ajustar o queryset do campo 'empresaprimaria'
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        if userid and type=='creat/edit':
            # self.fields['servico_agendado'].queryset = self.fields['servico_agendado'].queryset.filter(
            #     Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            #     status__in=['Agendado', 'Em andamento'],
            #     id_random=id_random
            # ).distinct()

            self.fields['servico_agendado'] = forms.ModelChoiceField(
                queryset=ServicoJardinagemAgendado.objects.filter(
                    Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                    status__in=['Agendado', 'Em andamento'],
                    id_random=id_random
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                    }
                ),
                label='Serviço agendado',
                required=True  # ou False, conforme sua lógica
            )

        if type == 'search':
            for field_name, field in self.fields.items():
                field.required = False

            # self.fields['servico_agendado'].queryset = self.fields['servico_agendado'].queryset.filter(
            #     Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
            #     Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
            # ).distinct()

            self.fields['servico_agendado'] = forms.ModelChoiceField(
                queryset=ServicoJardinagemAgendado.objects.filter(
                    Areas__localidade__unidade__empresasecundaria__empresaprimaria__id_random__in=empresas_primarias_ids,
                    Areas__localidade__unidade__empresasecundaria__id_random__in=empresas_secundarias_ids,
                ).distinct(),
                widget=forms.Select(
                    attrs={
                        'class': 'form-control',
                        'style': (
                            'max-height: 40px; overflow-y: auto; max-width: 600px; '
                            'white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'
                        )
                    }
                ),
                label='Serviço agendado',
                required=True  # ou False, conforme sua lógica
            )

    class Meta:
        model = CheckListJardinagem
        fields = ['servico_agendado', 'descricao', 'foto_comprovacao', 'status', ]

        labels = {
            'servico_agendado': 'Serviço agendado',
            'descricao': 'Descrição do checklist',
            'foto_comprovacao': 'Foto da entrega',
            'status': 'Status',
        }

        widgets = {
            # 'servico_agendado': forms.Select(
            #     attrs={
            #         'class': 'form-control'
            #     }
            # ),
            'descricao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'foto_comprovacao': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
