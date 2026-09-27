"""
ZeladorX Automações — plataforma interna da família ZeladorX.

Responsável por:
  * gerar os serviços automáticos (antes feito pela rota force_updates/ do app principal);
  * enviar as notificações por e-mail (atrasados, resumo diário, concluídos);
  * registrar cada execução para os times internos acompanharem.

Os apps compartilhados (areas, servicos, gerente, ...) são cópias fiéis do
repositório zeladorxV2 e NÃO devem ser alterados aqui. Somente os apps
exclusivos (automacoes, notificacoes_email, painel) têm migrações próprias.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

RODANDO_LOCAL = 'runserver' in sys.argv or os.getenv('AMBIENTE', 'local') == 'local'


def _env_bool(nome, padrao=False):
    valor = os.getenv(nome)
    if valor is None:
        return padrao
    return valor.strip().lower() in ('1', 'true', 'sim', 'yes', 'on')


# ============================================================
# SEGURANÇA / LOGIN COMPARTILHADO DA FAMÍLIA
# ============================================================

# Mesma chave e mesmo cookie do ZeladorX e do ChatChannels
SECRET_KEY_PADRAO = 'django-insecure-t+_dily3s3qm+@4k()5@$g3t&2$=6dvz-#h01i%@3t(7*4*!si'
SECRET_KEY = os.getenv('SECRET_KEY') or SECRET_KEY_PADRAO
SESSION_COOKIE_NAME = 'sessionid'
# Login compartilhado: a sessão guarda o caminho do backend usado no login.
# Precisa ser a MESMA lista do ZeladorX/ChatChannels; senão cada app descarta
# a sessão do outro (não loga automaticamente e desloga os demais).
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'gerente.backends.CaseInsensitiveModelBackend',
)
CSRF_COOKIE_DOMAIN = None if RODANDO_LOCAL else os.getenv('SESSION_COOKIE_DOMAIN', '.zeladorx.com.br')
SESSION_COOKIE_DOMAIN = None if RODANDO_LOCAL else os.getenv('SESSION_COOKIE_DOMAIN', '.zeladorx.com.br')

DEBUG = _env_bool('DEBUG', RODANDO_LOCAL)
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    o for o in os.getenv('CSRF_TRUSTED_ORIGINS', 'https://*.zeladorx.com.br,https://*.herokuapp.com').split(',') if o
]

SECURE_SSL_REDIRECT = not RODANDO_LOCAL
SESSION_COOKIE_SECURE = not RODANDO_LOCAL
CSRF_COOKIE_SECURE = not RODANDO_LOCAL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# ============================================================
# E-MAIL (Hostinger por padrão, tudo configurável por variável)
# ============================================================

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.hostinger.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = _env_bool('EMAIL_USE_TLS', EMAIL_PORT == 587)
EMAIL_USE_SSL = _env_bool('EMAIL_USE_SSL', EMAIL_PORT == 465) and not EMAIL_USE_TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'zeladorx@zeladorx.com.br')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_TIMEOUT = 20
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', f'ZeladorX <{EMAIL_HOST_USER}>')

# Segurança operacional: localmente os e-mails vão para o terminal,
# a menos que EMAIL_ENVIO_REAL=True. Evita disparar para os gerentes de teste.
EMAIL_ENVIO_REAL = _env_bool('EMAIL_ENVIO_REAL', not RODANDO_LOCAL)
EMAIL_BACKEND = (
    'django.core.mail.backends.smtp.EmailBackend' if EMAIL_ENVIO_REAL
    else 'django.core.mail.backends.console.EmailBackend'
)

# Link usado nos e-mails para abrir o app principal
ZELADORX_URL = os.getenv('ZELADORX_URL', 'http://127.0.0.1:8000' if RODANDO_LOCAL else 'https://app.zeladorx.com.br')


# ============================================================
# APPS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Apps compartilhados (cópia do zeladorxV2 — somente leitura)
    'areas.apps.AreasConfig',
    'catalogo_de_servicos.apps.CatalogoDeServicosConfig',
    'dashboards.apps.DashboardsConfig',
    'empresaprimaria.apps.EmpresaprimariaConfig',
    'empresasecundario.apps.EmpresasecundarioConfig',
    'gerente.apps.GerenteConfig',
    'localidade.apps.LocalidadeConfig',
    'notifications.apps.NotificationsConfig',
    'relatorios.apps.RelatoriosConfig',
    'terrenos.apps.TerrenosConfig',
    'unidade.apps.UnidadeConfig',
    'utils.apps.UtilsConfig',
    'vegetacao.apps.VegetacaoConfig',
    'servicos.apps.ServicosConfig',
    'settings.apps.SettingsConfig',
    'schedules.apps.SchedulesConfig',
    'semana.apps.SemanaConfig',
    'authenticate.apps.AuthenticateConfig',
    'permissionscontrol.apps.PermissionscontrolConfig',
    'zeladorx.apps.ZeladorxConfig',
    'checklists.apps.ChecklistsConfig',
    'medidor.apps.MedidorConfig',
    'retornos.apps.RetornosConfig',

    # Apps exclusivos desta plataforma
    'automacoes.apps.AutomacoesConfig',
    'notificacoes_email.apps.NotificacoesEmailConfig',
    'painel.apps.PainelConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# ============================================================
# BANCO (o mesmo do ZeladorX)
# ============================================================

if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=not RODANDO_LOCAL)}
elif os.getenv('USAR_SQLITE') == 'True':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'teste.sqlite3'}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_LOCAL_NAME', 'zeladorx'),
            'USER': os.getenv('DB_LOCAL_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_LOCAL_PASSWORD', 'PnCdEL'),
            'HOST': os.getenv('DB_LOCAL_HOST', 'localhost'),
            'PORT': os.getenv('DB_LOCAL_PORT', '5432'),
        }
    }

AUTH_USER_MODEL = 'gerente.Gerente'
LOGIN_URL = 'painel:login'
LOGIN_REDIRECT_URL = 'painel:inicio'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# IDIOMA / FUSO
# ============================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ============================================================
# ESTÁTICOS / MÍDIA
# ============================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {'automacoes': {'handlers': ['console'], 'level': 'INFO'},
                'notificacoes_email': {'handlers': ['console'], 'level': 'INFO'}},
}
