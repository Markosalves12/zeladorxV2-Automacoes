from django.contrib import admin
from medidor.models import DocsFromProcess

# Register your models here.
class DocsFromProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_random', 'document', )
    list_display_links = ('id', 'id_random', 'document', )
    search_fields = ('id', 'id_random', 'document', )

    list_per_page = 20


admin.site.register(DocsFromProcess, DocsFromProcessAdmin)