from django.contrib import admin
from checklists.models import CheckListLimpezaPredial, CheckListJardinagem

# Register your models here.
class CheckListLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'servico_agendado', 'descricao', 'status', )
    list_display_links = ('id', 'servico_agendado', 'descricao', 'status', )
    search_fields = ('status', )
    list_filter = ('status', )

    list_per_page = 20


admin.site.register(CheckListLimpezaPredial, CheckListLimpezaPredialAdmin)
admin.site.register(CheckListJardinagem, CheckListLimpezaPredialAdmin)
