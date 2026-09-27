from django.contrib import admin
from areas.models_jardinagem import AreasJardins
from areas.models_limpeza_predial import AreaLimpezaPredial

# Register your models here.
class AreasJardinsAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'foto', 'status', )
    list_display_links = ('id', 'nome', 'dimensao', 'Terreno', 'vegetacao', 'servico', 'localidade', 'foto', 'status', )
    search_fields = ('Terreno', 'vegetacao', 'servico', )
    list_filter = ('Terreno', 'vegetacao', 'servico', )

    list_per_page = 20

class AreasLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'dimensao', 'servico', 'localidade', 'foto', 'status',)
    list_display_links = ( 'id', 'nome', 'dimensao', 'servico', 'localidade', 'foto', 'status',)
    search_fields = ('servico',)
    list_filter = ('servico',)

    list_per_page = 20

admin.site.register(AreasJardins, AreasJardinsAdmin)
admin.site.register(AreaLimpezaPredial, AreasLimpezaPredialAdmin)