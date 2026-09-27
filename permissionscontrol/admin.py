from django.contrib import admin
from permissionscontrol.models import (PermissionsJardinagem, PermissionsAccessJardinagem,
                                       PermissionsAccessLimpezaPredial, PermissionsLimpezaPredial,
                                       PermissionsAccessEspecials, PermissionsEspecials)

# Register your models here.
class PermissionsJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Permissions', )
    list_display_links = ('id', 'Permissions', )

    list_per_page = 20

class PermissionsAccessJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gerente', )
    list_display_link = ('id', 'Gerente', )

    list_per_page = 20

class PermissionsLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'Permissions', )
    list_display_links = ('id', 'Permissions', )

    list_per_page = 20

class PermissionsAccessLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gerente', )
    list_display_link = ('id', 'Gerente', )

    list_per_page = 20

class PermissionsEspecialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Permissions', )
    list_display_links = ('id', 'Permissions', )

    list_per_page = 20

class PermissionsAccessEspecialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gerente', )
    list_display_link = ('id', 'Gerente', )

    list_per_page = 20


admin.site.register(PermissionsJardinagem, PermissionsJardinagemAdmin)
admin.site.register(PermissionsAccessJardinagem, PermissionsAccessJardinagemAdmin)
admin.site.register(PermissionsLimpezaPredial, PermissionsLimpezaPredialAdmin)
admin.site.register(PermissionsAccessLimpezaPredial, PermissionsAccessLimpezaPredialAdmin)
admin.site.register(PermissionsEspecials, PermissionsEspecialsAdmin)
admin.site.register(PermissionsAccessEspecials, PermissionsAccessEspecialsAdmin)
