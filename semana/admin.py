from django.contrib import admin
from semana.models import DiasDaSemana

# Register your models here.
class DiasDaSemanaAdmin(admin.ModelAdmin):
    list_display = ('diasdasemana', )


admin.site.register(DiasDaSemana, DiasDaSemanaAdmin)

# class DiasDasemanaAdmin(admin.ModelAdmin):
#     list_display = ('diasdasemana', )
#     list_filter = ('diasdasemana', )
#     list_display_links = ('diasdasemana', )
#
# admin.site.register(DiasDaSemana, DiasDasemanaAdmin)