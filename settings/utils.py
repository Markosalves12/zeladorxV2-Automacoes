from django.shortcuts import get_object_or_404
from gerente.forms_jardinagem import GerenteJardinagemForms
from settings.models import SettingServicosGerenteJardinagem, SettingServicosGerenteLimpezaPredial

def define_setting(request, model_class, email):
    objeto = get_object_or_404(model_class, email=email)
    print(objeto)

    # Jardinagem
    setting = SettingServicosGerenteJardinagem(
        Gerente=objeto
    )
    setting.save()

    # Limpeza
    setting = SettingServicosGerenteLimpezaPredial(
        Gerente=objeto,
    )
    setting.save()