from django import forms
from medidor.models import DocsFromProcess

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DocsFromProcess
        fields = ['document']
        labels = {
            'document': "Selecione um arquivo CSV ou Excel",
        }
        help_texts = {
            'document': "Formatos suportados: .csv, .xlsx",
        }
        widgets = {
            'document': forms.ClearableFileInput(attrs={"accept": ".csv, .xlsx"})
        }
