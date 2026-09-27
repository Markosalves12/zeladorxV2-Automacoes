from django.contrib import admin
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial

# Register your models here.
class CatalogodeServicoJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


class CatalogodeServicoLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    list_display_links = ('id', 'nome', 'EmpresaSecundaria', 'status', )
    search_fields = ('nome', 'EmpresaSecundaria', 'status', )
    list_filter = ('nome', 'EmpresaSecundaria', 'status', )

    list_per_page = 20


admin.site.register(CatalogodeServicoJardinagem, CatalogodeServicoJardinagemAdmin)
admin.site.register(CatalogodeServicoLimpezaPredial, CatalogodeServicoLimpezaPredialAdmin)