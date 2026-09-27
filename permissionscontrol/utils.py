from django.shortcuts import get_object_or_404
from permissionscontrol.models import (PermissionsAccessJardinagem,
                                       PermissionsAccessLimpezaPredial,
                                       PermissionsAccessEspecials)
from gerente.models import Gerente

def verify_login(request, userid):
    gerente = Gerente.objects.get(id_random=userid)
    if gerente.status == 'Desmobilizado':
        # messages.error(request, "usuario nao logado")
        return True

    return False

def configurate_permissions(request, model_class, email):
    objeto = get_object_or_404(model_class, email=email)
    # Jardinagem
    permissions = PermissionsAccessJardinagem(
        Gerente=objeto,
    )
    permissions.save()

    # limpeza predial
    permissions = PermissionsAccessLimpezaPredial(
        Gerente=objeto,
    )
    permissions.save()
    # especials

    permissions = PermissionsAccessEspecials(
        Gerente=objeto,
    )
    permissions.save()


def validate_permissions(request, userid, permission_type, permission_to_access):
    if Gerente.objects.get(id_random=userid).is_superuser == True:
        return True

    try:
        # Buscar as permissões associadas ao gerente com o id fornecido
        if permission_type == "jardinagem":
            permissions_instance = PermissionsAccessJardinagem.objects.get(
                Gerente__id_random=userid
            )

        elif permission_type == "limpeza_predial":
            permissions_instance = PermissionsAccessLimpezaPredial.objects.get(
                Gerente__id_random=userid
            )

        elif permission_type == "especials":
            permissions_instance = PermissionsAccessEspecials.objects.get(
                Gerente__id_random=userid
            )


    except:
        permissions_instance = []

    # print(type(permissions_instance))

    if isinstance(permissions_instance, PermissionsAccessJardinagem):
        # O objeto encontrado é um queryset (o que não é esperado aqui)
        if len(permissions_instance.Permissions.filter(Permissions__in=permission_to_access)) > 0:
            return True
        else:
            return False

    elif isinstance(permissions_instance, PermissionsAccessLimpezaPredial):
        # O objeto encontrado é um queryset (o que não é esperado aqui)
        if len(permissions_instance.Permissions.filter(Permissions__in=permission_to_access)) > 0:
            return True
        else:
            return False

    elif isinstance(permissions_instance, PermissionsAccessEspecials):
        if len(permissions_instance.Permissions.filter(Permissions__in=permission_to_access)) > 0:
            return True

    else:
        return True
