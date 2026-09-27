# admin.py
from django.contrib import admin
from .models import Gerente

@admin.register(Gerente)
class GerenteAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'password', 'status', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    list_filter = ('status', 'is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    filter_horizontal = ()  # Removido uso de 'groups' e 'user_permissions'
    fieldsets = (
        (None, {'fields': ('id_random', 'email', 'username',)}),
        ('Status e empresa', {'fields': ('status', 'empresasecundaria')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    readonly_fields = ('password',)