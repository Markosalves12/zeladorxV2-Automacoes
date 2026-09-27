from django.shortcuts import reverse

tipos = [
    {'nome': 'Jardinagem', 'link': reverse('localidades_jardinagem')},
    {'nome': 'Limpeza predial', 'link': reverse('localidades_limpeza_predial')},
]