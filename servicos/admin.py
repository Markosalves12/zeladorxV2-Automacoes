from django.contrib import admin

from servicos.models_limpeza_predial import (ServicoLimpezaPredialAgendado, ServicoLimpezaPredialConfigurado,
                                             FatoServicoLimpezaPredial)
from servicos.models_jardinagem import ServicoJardinagemAgendado, FatoServicoJardinagem, ServicoJardinagemConfigurado

from servicos.admin_jardinagem import (ServicoJardinagemAgendadoAdmin, FatoServicoJardinagemAdmin,
                                       ServicoJardinagemConfiguradoAdmin)
from servicos.admin_limpeza_predial import (ServicoLimpezaPredialAgendadoAdmin, ServicoLimpezaPredialConfiguradoAdmin,
                                            FatoServicoLimpezaPredialAdmin)


admin.site.register(ServicoJardinagemConfigurado, ServicoJardinagemConfiguradoAdmin)
admin.site.register(FatoServicoJardinagem, FatoServicoJardinagemAdmin)
admin.site.register(ServicoJardinagemAgendado, ServicoJardinagemAgendadoAdmin)


admin.site.register(ServicoLimpezaPredialAgendado, ServicoLimpezaPredialAgendadoAdmin)
admin.site.register(ServicoLimpezaPredialConfigurado, ServicoLimpezaPredialConfiguradoAdmin)
admin.site.register(FatoServicoLimpezaPredial, FatoServicoLimpezaPredialAdmin)