from django.db import models
from utils.utils import generate_id_random
from gerente.models import Gerente

# Create your models here.
class PermissionsJardinagem(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    permissions_CRUD = [
        ('250: Pode criar novas áreas de jardinagem', '250: Pode criar novas áreas de jardinagem'),
        ('251: Pode editar áreas de jardinagem', '251: Pode editar áreas de jardinagem'),
        ('252: Pode visualizar áreas de jardinagem', '252: Pode visualizar áreas de jardinagem'),
        ('253: Pode excluir áreas de jardinagem', '253: Pode excluir áreas de jardinagem'),
        ('254: Pode desmobilizar áreas de jardinagem', '254: Pode desmobilizar áreas de jardinagem'),
        ('255: Pode reabilitar áreas de jardinagem', '255: Pode reabilitar áreas de jardinagem'),

        ('260: Pode criar novos serviços ao catálogo', '260: Pode criar novos serviços ao catálogo'),
        ('261: Pode editar serviços do catálogo', '261: Pode editar serviços do catálogo'),
        ('262: Pode visualizar serviços do catálogo', '262: Pode visualizar serviços do catálogo'),
        ('263: Pode excluir serviços do catálogo', '263: Pode excluir serviços do catálogo'),
        ('264: Pode desmobilizar serviços do catálogo', '264: Pode desmobilizar serviços do catálogo'),
        ('265: Pode reabilitar serviços do catálogo', '265: Pode reabilitar serviços do catálogo'),

        ('280: Pode criar novos colaboradores', '280: Pode criar novos colaboradores'),
        ('281: Pode editar colaboradores', '281: Pode editar colaboradores'),
        ('282: Pode visualizar colaboradores', '282: Pode visualizar colaboradores'),
        ('283: Pode excluir colaboradores', '283: Pode excluir colaboradores'),
        ('284: Pode desmobilizar colaboradores', '284: Pode desmobilizar colaboradores'),
        ('285: Pode reabilitar colaboradores', '285: Pode reabilitar colaboradores'),

        ('290: Pode criar novas localidades', '290: Pode criar novas localidades'),
        ('291: Pode editar localidades', '291: Pode editar localidades'),
        ('292: Pode visualizar localidades', '292: Pode visualizar localidades'),
        ('293: Pode excluir localidades', '293: Pode excluir localidades'),
        ('294: Pode desmobilizar localidades', '294: Pode desmobilizar localidades'),
        ('295: Pode reabilitar localidades', '295: Pode reabilitar localidades'),

        ('300: Pode editar permissões de jardinagem', '300: Pode editar permissões de jardinagem'),
        ('301: Pode visualizar permissões de jardinagem', '301: Pode visualizar permissões de jardinagem'),

        ('310: Pode extrair relatórios XLSX de jardinagem', '310: Pode extrair relatórios XLSX de jardinagem'),
        ('311: Pode extrair relatórios PDF de jardinagem', '311: Pode extrair relatórios PDF de jardinagem'),

        ('320: Pode agendar novos serviços', '320: Pode agendar novos serviços'),
        ('321: Pode editar serviços agendados', '321: Pode editar serviços agendados'),
        ('322: Pode visualizar serviços agendados', '322: Pode visualizar serviços agendados'),
        ('323: Pode excluir serviços agendados', '323: Pode excluir serviços agendados'),
        ('324: Pode acompanhar serviços agendados', '324: Pode acompanhar serviços agendados'),
        ('325: Pode editar serviços em andamento', '325: Pode editar serviços em andamento'),
        ('326 Pode concluir serviços em andamento', '326: Pode concluir serviços em andamento'),
        ('327 Pode excluir serviços concluidos', '327: Pode excluir serviços concluidos'),
        ('328: Pode cancelar serviços agendados', '328: Pode cancelar serviços agendados'),

        ('330: Pode criar novos terrenos', '330: Pode criar novos terrenos'),
        ('331: Pode editar terrenos', '331: Pode editar terrenos'),
        ('332: Pode visualizar terrenos', '332: Pode visualizar terrenos'),
        ('333: Pode excluir terrenos', '333: Pode excluir terrenos'),
        ('334: Pode desmobilizar terrenos', '334: Pode desmobilizar terrenos'),
        ('335: Pode reabilitar terrenos', '335: Pode reabilitar terrenos'),

        ('350: Pode criar novas vegetações', '350: Pode criar novas vegetações'),
        ('351: Pode editar vegetações', '351: Pode editar vegetações'),
        ('352: Pode visualizar vegetações', '352: Pode visualizar vegetações'),
        ('353: Pode excluir vegetações', '353: Pode excluir vegetações'),
        ('354: Pode desmobilizar vegetações', '354: Pode desmobilizar vegetações'),
        ('355: Pode reabilitar vegetações', '355: Pode reabilitar vegetações'),

        ('360: Recebe serviços de jardinagem', '360: Recebe serviços de jardinagem'),
        ('361: Pode acompanhar serviços agendados para si próprio',
         '361: Pode acompanhar serviços agendados para si próprio'),

        ('370: Pode configurar novos serviços', '370: Pode configurar novos serviços'),
        ('371: Pode editar serviços configurados', '371: Pode editar serviços configurados'),
        ('372: Pode visualizar serviços configurados', '372: Pode visualizar serviços configurados'),
        ('373: Pode excluir serviços configurados', '373: Pode excluir serviços configurados'),
        ('374: Pode desmobilizar serviços configurados', '374: Pode desmobilizar serviços configurados'),
        ('375: Pode reabilitar serviços configurados', '375: Pode reabilitar serviços configurados'),

        ('380: Pode visualizar o dashboard gerencial', '380: Pode visualizar o dashboard gerencial'),
        ('381: Pode visualizar o dashboard administrativo', '381: Pode visualizar o dashboard administrativo'),

        ('390: Pode visualizar o detalhamento de serviços', '390: Pode visualizar o detalhamento de serviços'),
        ('391: Pode editar o acompanhamento de servicos', '391: Pode editar o acompanhamento de servicos'),

        ('400: Pode criar novos checklists', '400: Pode criar novos checklists'),
        ('401: Pode editar checklists', '401: Pode editar checklists'),
        ('402: Pode visualizar checklists', '402: Pode visualizar checklists'),
        ('403: Pode excluir checklists', '403: Pode excluir checklists'),

        ('410: Pode editar o recebimento de notificações gerais',
         '410: Pode editar o recebimento de notificações gerais'),
        ('411: Pode editar o recebimento de notificações individuais',
         '411: Pode editar o recebimento de notificações individuais'),

        ('420: Pode criar QR codes', '420: Pode criar QR codes'),
        ('421: Pode editar QR codes', '421: Pode editar QR codes'),
        ('422: Pode visualizar QR codes', '422: Pode visualizar QR codes'),
        ('423: Pode excluir QR codes', '423: Pode excluir QR codes'),
        ('424: Pode desmobilizar QR codes', '424: Pode desmobilizar QR codes'),
        ('425: Pode reabilitar QR codes', '425: Pode reabilitar QR codes'),

        ('431: Pode editar solicitacoes', '431: Pode editar solicitacoes'),
        ('432: Pode visualizar solicitacoes', '432: Pode visualizar solicitacoes'),
        ('433: Pode excluir solicitacoes', '433: Pode excluir solicitacoes'),
        ('434: Pode Rejeitar/aceitar solicitacoes', '434: Pode Rejeitar/aceitar solicitacoes'),
    ]

    Permissions = models.CharField(
        choices=permissions_CRUD,
        null=False,
        blank=False,
        unique=True,
        max_length=75
    )

    def __str__(self):
        return self.Permissions


class PermissionsAccessJardinagem(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    Permissions = models.ManyToManyField(
        to=PermissionsJardinagem,
        null=False,
        blank=False,
        related_name='RPermissionsAccessJardinagem'
    )

class PermissionsLimpezaPredial(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    permissions_CRUD = [
        ('250: Pode criar novas áreas de limpeza predial', '250: Pode criar novas áreas de limpeza predial'),
        ('251: Pode editar áreas de limpeza predial', '251: Pode editar áreas de limpeza predial'),
        ('252: Pode visualizar áreas de limpeza predial', '252: Pode visualizar áreas de limpeza predial'),
        ('253: Pode excluir áreas de limpeza predial', '253: Pode excluir áreas de limpeza predial'),
        ('254: Pode desmobilizar áreas de limpeza predial', '254: Pode desmobilizar áreas de limpeza predial'),
        ('255: Pode reabilitar áreas de limpeza predial', '255: Pode reabilitar áreas de limpeza predial'),

        ('260: Pode criar novos serviços ao catálogo', '260: Pode criar novos serviços ao catálogo'),
        ('261: Pode editar serviços do catálogo', '261: Pode editar serviços do catálogo'),
        ('262: Pode visualizar serviços do catálogo', '262: Pode visualizar serviços do catálogo'),
        ('263: Pode excluir serviços do catálogo', '263: Pode excluir serviços do catálogo'),
        ('264: Pode desmobilizar serviços do catálogo', '264: Pode desmobilizar serviços do catálogo'),
        ('265: Pode reabilitar serviços do catálogo', '265: Pode reabilitar serviços do catálogo'),

        ('280: Pode criar novos colaboradores', '280: Pode criar novos colaboradores'),
        ('281: Pode editar colaboradores', '281: Pode editar colaboradores'),
        ('282: Pode visualizar colaboradores', '282: Pode visualizar colaboradores'),
        ('283: Pode excluir colaboradores', '283: Pode excluir colaboradores'),
        ('284: Pode desmobilizar colaboradores', '284: Pode desmobilizar colaboradores'),
        ('285: Pode reabilitar colaboradores', '285: Pode reabilitar colaboradores'),

        ('290: Pode criar novas localidades', '290: Pode criar novas localidades'),
        ('291: Pode editar localidades', '291: Pode editar localidades'),
        ('292: Pode visualizar localidades', '292: Pode visualizar localidades'),
        ('293: Pode excluir localidades', '293: Pode excluir localidades'),
        ('294: Pode desmobilizar localidades', '294: Pode desmobilizar localidades'),
        ('295: Pode reabilitar localidades', '295: Pode reabilitar localidades'),

        ('300: Pode editar permissões de limpeza predial', '300: Pode editar permissões de limpeza predial'),
        ('301: Pode visualizar permissões de limpeza predial', '301: Pode visualizar permissões de limpeza predial'),

        ('310: Pode extrair relatórios XLSX de limpeza predial', '310: Pode extrair relatórios XLSX de limpeza predial'),
        ('311: Pode extrair relatórios PDF de limpeza predial', '311: Pode extrair relatórios PDF de limpeza predial'),

        ('320: Pode agendar novos serviços', '320: Pode agendar novos serviços'),
        ('321: Pode editar serviços agendados', '321: Pode editar serviços agendados'),
        ('322: Pode visualizar serviços agendados', '322: Pode visualizar serviços agendados'),
        ('323: Pode excluir serviços agendados', '323: Pode excluir serviços agendados'),
        ('324: Pode acompanhar serviços agendados', '324: Pode acompanhar serviços agendados'),
        ('325: Pode editar serviços em andamento', '325: Pode editar serviços em andamento'),
        ('326 Pode concluir serviços em andamento', '326: Pode concluir serviços em andamento'),
        ('327 Pode excluir serviços concluidos', '327: Pode excluir serviços concluidos'),
        ('328: Pode cancelar serviços agendados', '328: Pode cancelar serviços agendados'),

        ('360: Recebe serviços de limpeza predial', '360: Recebe serviços de limpeza predial'),
        ('361: Pode acompanhar serviços agendados para si próprio', '361: Pode acompanhar serviços agendados para si próprio'),

        ('370: Pode configurar novos serviços', '370: Pode configurar novos serviços'),
        ('371: Pode editar serviços configurados', '371: Pode editar serviços configurados'),
        ('372: Pode visualizar serviços configurados', '372: Pode visualizar serviços configurados'),
        ('373: Pode excluir serviços configurados', '373: Pode excluir serviços configurados'),
        ('374: Pode desmobilizar serviços configurados', '374: Pode desmobilizar serviços configurados'),
        ('375: Pode reabilitar serviços configurados', '375: Pode reabilitar serviços configurados'),

        ('380: Pode visualizar o dashboard gerencial', '380: Pode visualizar o dashboard gerencial'),
        ('381: Pode visualizar o dashboard administrativo', '381: Pode visualizar o dashboard administrativo'),

        ('390: Pode visualizar o detalhamento de serviços', '390: Pode visualizar o detalhamento de serviços'),
        ('391: Pode editar o acompanhamento de servicos', '391: Pode editar o acompanhamento de servicos'),

        ('400: Pode criar novos checklists', '400: Pode criar novos checklists'),
        ('401: Pode editar checklists', '401: Pode editar checklists'),
        ('402: Pode visualizar checklists', '402: Pode visualizar checklists'),
        ('403: Pode excluir checklists', '403: Pode excluir checklists'),

        ('410: Pode editar o recebimento de notificações gerais',
         '410: Pode editar o recebimento de notificações gerais'),
        ('411: Pode editar o recebimento de notificações individuais',
         '411: Pode editar o recebimento de notificações individuais'),

        ('420: Pode criar QR codes', '420: Pode criar QR codes'),
        ('421: Pode editar QR codes', '421: Pode editar QR codes'),
        ('422: Pode visualizar QR codes', '422: Pode visualizar QR codes'),
        ('423: Pode excluir QR codes', '423: Pode excluir QR codes'),
        ('424: Pode desmobilizar QR codes', '424: Pode desmobilizar QR codes'),
        ('425: Pode reabilitar QR codes', '425: Pode reabilitar QR codes'),

        ('431: Pode editar solicitacoes', '431: Pode editar solicitacoes'),
        ('432: Pode visualizar solicitacoes', '432: Pode visualizar solicitacoes'),
        ('433: Pode excluir solicitacoes', '433: Pode excluir solicitacoes'),
        ('434: Pode Rejeitar/aceitar solicitacoes', '434: Pode Rejeitar/aceitar solicitacoes'),
    ]

    Permissions = models.CharField(
        choices=permissions_CRUD,
        null=False,
        blank=False,
        unique=True,
        max_length=75
    )

    def __str__(self):
        return self.Permissions


class PermissionsAccessLimpezaPredial(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    Permissions = models.ManyToManyField(
        to=PermissionsLimpezaPredial,
        null=False,
        blank=False,
        related_name='RPermissionsAccessLimpezaPredial'
    )

class PermissionsEspecials(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    permissions_CRUD = [
        ('270: Pode criar novas empresas', '270: Pode criar novas empresas'),
        ('271: Pode editar empresas', '271: Pode editar empresas'),
        ('272: Pode visualizar empresas', '272: Pode visualizar empresas'),
        ('273: Pode excluir empresas', '273: Pode excluir empresas'),
        ('274: Pode desmobilizar empresas', '274: Pode desmobilizar empresas'),
        ('275: Pode reabilitar empresas', '275: Pode reabilitar empresas'),

        ('300: Pode editar permissões especiais', '300: Pode editar permissões especiais'),
        ('301: Pode visualizar permissões especiais', '301: Pode visualizar permissões especiais'),

        ('340: Pode criar novas unidades', '340: Pode criar novas unidades'),
        ('341: Pode editar unidades', '341: Pode editar unidades'),
        ('342: Pode visualizar unidades', '342: Pode visualizar unidades'),
        ('343: Pode excluir unidades', '343: Pode excluir unidades'),
        ('344: Pode desmobilizar unidades', '344: Pode desmobilizar unidades'),
        ('345: Pode reabilitar unidades', '345: Pode reabilitar unidades'),
    ]

    Permissions = models.CharField(
        choices=permissions_CRUD,
        null=False,
        blank=False,
        unique=True,
        max_length=75
    )

    def __str__(self):
        return self.Permissions


class PermissionsAccessEspecials(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    Permissions = models.ManyToManyField(
        to=PermissionsEspecials,
        null=False,
        blank=False,
        related_name='RPermissionsAccessEspecials'
    )
