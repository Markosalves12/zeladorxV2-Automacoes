from django.contrib import admin
from vegetacao.models import CatalogoVegetacao

# Register your models here.
class CatalogoVegetacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


admin.site.register(CatalogoVegetacao, CatalogoVegetacaoAdmin)