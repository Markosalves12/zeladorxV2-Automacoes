from django.contrib import admin
from localidade.models_Jardinagem import LocalidadeJardiangem
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial

# Register your models here.
class LocalidadeJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'lat_med', 'long_med', 'unidade', 'status', )
    list_display_links = ('id', 'nome', 'lat_med', 'long_med', 'unidade', 'status', )
    search_fields = ('nome', )
    list_filter = ('nome', )

    list_per_page = 20

class LocalidadeLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'lat_med', 'long_med', 'unidade', 'status', )
    list_display_links = ('id', 'nome', 'lat_med', 'long_med', 'unidade', 'status', )
    search_fields = ('nome', )
    list_filter = ('nome', )

    list_per_page = 20

admin.site.register(LocalidadeJardiangem, LocalidadeJardinagemAdmin)
admin.site.register(LocalidadeLimpezaPredial, LocalidadeLimpezaPredialAdmin)