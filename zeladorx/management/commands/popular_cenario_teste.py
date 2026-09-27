"""
Popula o banco com o cenário completo de teste do ZeladorX.

Cenário: a Vitória Tech fornece o ZeladorX para 15 prefeituras do Espírito Santo.
Prefeituras -> empresas primárias | secretarias/equipes -> empresas secundárias |
usuários -> gerentes (todos superusuários, senha 1234).

Uso:
    python manage.py popular_cenario_teste               # cria o cenário
    python manage.py popular_cenario_teste --reset       # apaga o cenário e recria
    python manage.py popular_cenario_teste --apagar      # só apaga o cenário
    python manage.py popular_cenario_teste --seed 7 --servicos-por-area 20

Heroku:
    heroku run python manage.py popular_cenario_teste --reset -a <app>

Não cria migração e não altera nenhum model. Tudo que o script cria é
identificado pelos nomes das prefeituras e pelo domínio de e-mail
@teste.zeladorx.com.br, então o --reset só apaga o que ele mesmo criou.
"""
import random
from datetime import datetime, time, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from areas.models_jardinagem import AreasJardins
from areas.models_limpeza_predial import AreaLimpezaPredial
from catalogo_de_servicos.models_jardinagem import CatalogodeServicoJardinagem
from catalogo_de_servicos.models_limpeza_predial import CatalogodeServicoLimpezaPredial
from checklists.models import CheckListJardinagem, CheckListLimpezaPredial
from empresaprimaria.models import EmpresaPrimaria
from empresasecundario.models import EmpresaSecundaria
from gerente.models import Gerente
from localidade.models_Jardinagem import LocalidadeJardiangem
from localidade.models_limpeza_predial import LocalidadeLimpezaPredial
from permissionscontrol.models import (
    PermissionsAccessEspecials,
    PermissionsAccessJardinagem,
    PermissionsAccessLimpezaPredial,
    PermissionsEspecials,
    PermissionsJardinagem,
    PermissionsLimpezaPredial,
)
from semana.models import DiasDaSemana
from servicos.models_jardinagem import (
    FatoServicoJardinagem,
    ServicoJardinagemAgendado,
    ServicoJardinagemConfigurado,
)
from servicos.models_limpeza_predial import (
    FatoServicoLimpezaPredial,
    ServicoLimpezaPredialAgendado,
    ServicoLimpezaPredialConfigurado,
)
from terrenos.models import Terreno
from unidade.models import Unidade
from vegetacao.models import CatalogoVegetacao
from zeladorx.models import TypeZeladoria


DOMINIO_EMAIL = 'teste.zeladorx.com.br'
SENHA_PADRAO = '1234'

JARDINAGEM = 'Jardinagem'
LIMPEZA = 'Limpeza predial'

# ---------------------------------------------------------------------------
# Dados do cenário
# ---------------------------------------------------------------------------

# nome, lat, long, distritos, bairros da sede
MUNICIPIOS = [
    ('Vitória', -20.3155, -40.3128, ['Ilha do Boi', 'Goiabeiras'],
     ['Centro', 'Jardim Camburi', 'Praia do Canto', 'Jardim da Penha', 'Bento Ferreira']),
    ('Vila Velha', -20.3297, -40.2925, ['Ibes', 'Jucu', 'Argolas'],
     ['Centro', 'Praia da Costa', 'Itapoã', 'Glória']),
    ('Serra', -20.1286, -40.3078, ['Carapina', 'Calogi', 'Nova Almeida'],
     ['Serra Sede', 'Laranjeiras', 'Jacaraípe', 'Manguinhos']),
    ('Cariacica', -20.2632, -40.4165, ['Itaquari', 'Roças Velhas'],
     ['Campo Grande', 'Jardim América', 'Alto Lage']),
    ('Guarapari', -20.6717, -40.4997, ['Todos os Santos', 'Rio Calçado'],
     ['Centro', 'Praia do Morro', 'Muquiçaba']),
    ('Linhares', -19.3946, -40.0643, ['Regência', 'Bebedouro'],
     ['Centro', 'Interlagos', 'Shell', 'Aviso']),
    ('Colatina', -19.5390, -40.6305, ['Baunilha', 'Itapina'],
     ['Centro', 'Esplanada', 'São Silvano']),
    ('Cachoeiro de Itapemirim', -20.8489, -41.1129, ['Burarama', 'Pacotuba'],
     ['Centro', 'Aquidabã', 'Gilberto Machado', 'Independência']),
    ('São Mateus', -18.7214, -39.8579, ['Guriri', 'Nestor Gomes'],
     ['Centro', 'Sernamby', 'Boa Vista']),
    ('Aracruz', -19.8203, -40.2733, ['Santa Cruz', 'Barra do Riacho'],
     ['Centro', 'Coqueiral', 'Vila Rica']),
    ('Viana', -20.3900, -40.4960, ['Araçatiba'],
     ['Centro', 'Marcílio de Noronha', 'Areinha']),
    ('Nova Venécia', -18.7150, -40.4053, ['Guararema'],
     ['Centro', 'Bom Jesus', 'Rúbia']),
    ('Domingos Martins', -20.3633, -40.6594, ['Paraju', 'Melgaço'],
     ['Centro', 'Campinho', 'Vila Verde']),
    ('Santa Teresa', -19.9363, -40.6003, ['São João de Petrópolis'],
     ['Centro', 'Vila Nova', 'Jardim da Montanha']),
    ('Anchieta', -20.8053, -40.6425, ['Jabaquara', 'Alto Pongal'],
     ['Centro', 'Castelhanos', 'Iriri']),
]

# modelos de times: (nome curto — cabe em 40 caracteres, setores)
TIMES = [
    ('SEMMAM Parques e Jardins', [JARDINAGEM]),
    ('SEMOB Prédios Públicos', [LIMPEZA]),
    ('SEMSU Zeladoria Urbana', [JARDINAGEM, LIMPEZA]),
    ('SEMED Escolas', [LIMPEZA]),
    ('APP e Reflorestamento', [JARDINAGEM]),
]

CATALOGO_JARDINAGEM = [
    'Poda de árvores', 'Poda de arbustos', 'Roçada mecanizada', 'Roçada manual',
    'Capina química', 'Capina manual', 'Replantio de mudas', 'Plantio de gramas',
    'Adubação', 'Irrigação', 'Limpeza de canteiros', 'Supressão de árvore',
    'Controle de formigas', 'Recolhimento de resíduos verdes',
]

CATALOGO_LIMPEZA = [
    'Limpeza de pisos', 'Limpeza de banheiros', 'Limpeza de vidros',
    'Recolhimento de lixo', 'Higienização de bebedouros', 'Limpeza de fachada',
    'Desinfecção de ambientes', 'Limpeza de caixa d’água', 'Enceramento',
    'Limpeza pós-obra',
]

VEGETACOES = [
    'Grama esmeralda', 'Grama batatais', 'Ipê-amarelo', 'Ipê-roxo', 'Pau-brasil',
    'Palmeira-imperial', 'Coqueiro', 'Oiti', 'Aroeira', 'Jacarandá',
    'Restinga nativa', 'Mata Atlântica secundária', 'Buxinho', 'Moreia',
    'Pingo-de-ouro', 'Helicônia',
]

TIPOS_AREA_JARDINAGEM = [
    ('Praça', 800, 6000), ('Canteiro central da Av.', 300, 2500),
    ('Parque Municipal', 8000, 60000), ('APP', 5000, 90000),
    ('Rotatória', 100, 900), ('Jardim da Escola', 200, 1500),
    ('Orla', 2000, 20000), ('Cemitério Municipal', 3000, 15000),
]

TIPOS_AREA_LIMPEZA = [
    ('Prédio da Prefeitura', 1500, 6000), ('UBS', 400, 1500),
    ('EMEF', 800, 3500), ('CRAS', 300, 900), ('Biblioteca Municipal', 400, 1200),
    ('Ginásio Poliesportivo', 1500, 5000), ('Câmara Municipal', 800, 3000),
]

NOMES_PROPRIOS = [
    'Getúlio Vargas', 'Costa Pereira', 'Oito de Maio', 'dos Namorados', 'São Pedro',
    'da Paz', 'Jerônimo Monteiro', 'Maria Ortiz', 'do Cruzeiro', 'Santa Luzia',
    'dos Pescadores', 'da Juventude', 'Florentino Avidos', 'do Rosário',
]

CHECKLIST_JARDINAGEM = {
    'Poda': ['Isolar a área com cones', 'Conferir EPIs da equipe', 'Executar poda',
             'Recolher galhos', 'Registrar foto final'],
    'Roçada': ['Sinalizar a via', 'Retirar pedras e lixo', 'Roçar a área',
               'Varrer calçadas', 'Registrar foto final'],
    'Capina': ['Conferir EPI e pulverizador', 'Aplicar herbicida nas juntas',
               'Registrar dosagem aplicada', 'Registrar foto final'],
    'Replantio': ['Abrir berços', 'Adubar berços', 'Plantar mudas', 'Tutorar mudas',
                  'Irrigar'],
    'default': ['Conferir EPIs', 'Executar serviço', 'Limpar a área',
                'Registrar foto final'],
}

CHECKLIST_LIMPEZA = ['Conferir material de limpeza', 'Varrer e aspirar',
                     'Higienizar sanitários', 'Retirar lixo', 'Registrar foto final']

# gerentes que participam de mais de uma prefeitura (username, e-mail, prefeituras)
GERENTES_MULTI = [
    ('micaelle', 'micaelle', ['Vitória', 'Vila Velha']),
    ('Carlos Fiscal', 'carlos.fiscal', ['Serra', 'Cariacica', 'Viana']),
    ('Ana Paula Supervisora', 'ana.paula', ['Guarapari', 'Anchieta']),
    ('Rodrigo Encarregado', 'rodrigo', ['Linhares', 'Aracruz', 'São Mateus']),
    ('Juliana Gestora', 'juliana', ['Colatina', 'Nova Venécia']),
    ('Marcos Consultor', 'marcos', ['Cachoeiro de Itapemirim', 'Domingos Martins',
                                     'Santa Teresa']),
    ('Fernanda Fiscal', 'fernanda', ['Vitória', 'Serra', 'Vila Velha', 'Cariacica']),
    ('Tiago Supervisor', 'tiago', ['Domingos Martins', 'Santa Teresa']),
    ('Beatriz Gestora', 'beatriz', ['Aracruz', 'Linhares']),
    ('Vitória Tech Suporte', 'suporte', [m[0] for m in MUNICIPIOS]),
]

PRIMEIROS_NOMES = ['João', 'Maria', 'José', 'Luana', 'Pedro', 'Camila', 'Rafael',
                   'Larissa', 'Bruno', 'Patrícia', 'Diego', 'Renata', 'Felipe',
                   'Aline', 'Gustavo', 'Sabrina', 'Leandro', 'Tatiane', 'Eduardo',
                   'Priscila']
SOBRENOMES = ['Silva', 'Souza', 'Oliveira', 'Santos', 'Lima', 'Pereira', 'Costa',
              'Ferreira', 'Rodrigues', 'Almeida', 'Nascimento', 'Carvalho']

HORARIOS = [time(7, 0), time(7, 30), time(8, 0), time(9, 0), time(10, 0),
            time(13, 0), time(14, 0), time(15, 30)]

PERIODICIDADES = ['Semanal', 'Quinzenal', 'Mensal', 'Mensal', 'Bimestral',
                  'Trimestral', 'Semestral']


def nome_prefeitura(municipio):
    artigo = 'da' if municipio == 'Serra' else 'de'
    return f'Prefeitura {artigo} {municipio}'


NOMES_PREFEITURAS = [nome_prefeitura(m[0]) for m in MUNICIPIOS]


class Command(BaseCommand):
    help = 'Popula o banco com o cenário de teste (15 prefeituras do ES).'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                            help='Apaga o cenário existente antes de criar.')
        parser.add_argument('--apagar', action='store_true',
                            help='Apenas apaga o cenário, sem recriar.')
        parser.add_argument('--seed', type=int, default=42)
        parser.add_argument('--servicos-por-area', type=int, default=18,
                            help='Média de serviços agendados por área (padrão 18).')
        parser.add_argument('--meses-historico', type=int, default=18)
        parser.add_argument('--meses-futuro', type=int, default=3)

    # ------------------------------------------------------------------
    def handle(self, *args, **opts):
        self.rng = random.Random(opts['seed'])
        self.agora = timezone.now()

        existe = EmpresaPrimaria.objects.filter(nome__in=NOMES_PREFEITURAS).exists()

        if opts['apagar'] or opts['reset']:
            self.apagar()
            if opts['apagar']:
                return
        elif existe:
            self.stdout.write(self.style.WARNING(
                'O cenário já existe. Use --reset para recriar ou --apagar para remover.'))
            return

        self.garantir_base()

        with transaction.atomic():
            self.criar_estrutura()
            self.criar_gerentes()
            self.criar_permissoes_gerentes()
            self.criar_servicos(opts)

        self.resumo()

    # ------------------------------------------------------------------
    def log(self, texto):
        self.stdout.write(f'  • {texto}')

    def apagar(self):
        self.stdout.write('Apagando cenário de teste...')
        with transaction.atomic():
            gerentes = Gerente.objects.filter(email__endswith=f'@{DOMINIO_EMAIL}')
            self.log(f'{gerentes.count()} gerentes')
            gerentes.delete()

            unidades = Unidade.objects.filter(
                empresasecundaria__empresaprimaria__nome__in=NOMES_PREFEITURAS).distinct()
            self.log(f'{unidades.count()} unidades (com localidades, áreas e serviços)')
            Unidade.objects.filter(pk__in=list(unidades.values_list('pk', flat=True))).delete()

            empresas = EmpresaPrimaria.objects.filter(nome__in=NOMES_PREFEITURAS)
            self.log(f'{empresas.count()} prefeituras (com times, catálogos, terrenos e vegetações)')
            empresas.delete()
        self.stdout.write(self.style.SUCCESS('Cenário apagado.'))

    def garantir_base(self):
        self.setor = {
            JARDINAGEM: TypeZeladoria.objects.get_or_create(setor=JARDINAGEM)[0],
            LIMPEZA: TypeZeladoria.objects.get_or_create(setor=LIMPEZA)[0],
        }
        self.dias = [DiasDaSemana.objects.get_or_create(diasdasemana=d[0])[0]
                     for d in DiasDaSemana._meta.get_field('diasdasemana').choices]
        try:
            call_command('criar_permissoes', verbosity=0)
        except Exception as erro:  # comando pode não existir em versões antigas
            self.stdout.write(self.style.WARNING(f'criar_permissoes não executado: {erro}'))

    # ------------------------------------------------------------------
    def jitter(self, valor, raio=0.03):
        return round(valor + self.rng.uniform(-raio, raio), 6)

    def criar_estrutura(self):
        self.stdout.write('Criando prefeituras, times e locais...')
        rng = self.rng
        self.prefeituras = {}
        self.times_por_prefeitura = {}
        self.areas_j, self.areas_l = [], []
        self.catalogo_j, self.catalogo_l = {}, {}

        for indice, (municipio, lat, lon, distritos, bairros) in enumerate(MUNICIPIOS):
            unidades_nomes = ['Sede'] + distritos
            primaria = EmpresaPrimaria.objects.create(
                nome=nome_prefeitura(municipio),
                N_unidades=len(unidades_nomes),
                status='Mobilizado',
            )
            primaria.setor.set(self.setor.values())
            self.prefeituras[municipio] = primaria

            # 2 a 4 times por prefeitura, sempre com jardinagem e limpeza cobertos
            quantidade = 2 + indice % 3
            modelos = {2: [TIMES[2], TIMES[0]], 3: TIMES[:3], 4: TIMES[:4]}[quantidade]

            times = []
            for nome, setores in modelos:
                time_obj = EmpresaSecundaria.objects.create(
                    nome=nome, empresaprimaria=primaria, status='Mobilizado')
                time_obj.setor.set([self.setor[s] for s in setores])
                time_obj.setores = setores
                times.append(time_obj)
            self.times_por_prefeitura[municipio] = times

            times_j = [t for t in times if JARDINAGEM in t.setores]
            times_l = [t for t in times if LIMPEZA in t.setores]

            # catálogos, vegetações e terrenos por time
            recursos = {}
            for t in times_j:
                servicos = CatalogodeServicoJardinagem.objects.bulk_create([
                    CatalogodeServicoJardinagem(nome=n, EmpresaSecundaria=t)
                    for n in CATALOGO_JARDINAGEM])
                vegetacoes = CatalogoVegetacao.objects.bulk_create([
                    CatalogoVegetacao(nome=n, EmpresaSecundaria=t)
                    for n in rng.sample(VEGETACOES, 8)])
                terrenos = Terreno.objects.bulk_create([
                    Terreno(nome=f'Talhão {letra}', EmpresaSecundaria=t)
                    for letra in 'ABCDE'])
                self.catalogo_j[t.pk] = servicos
                recursos[t.pk] = (servicos, vegetacoes, terrenos)
            for t in times_l:
                self.catalogo_l[t.pk] = CatalogodeServicoLimpezaPredial.objects.bulk_create([
                    CatalogodeServicoLimpezaPredial(nome=n, EmpresaSecundaria=t)
                    for n in CATALOGO_LIMPEZA])

            # unidades (sede e distritos), localidades e áreas
            for nome_unidade in unidades_nomes:
                unidade = Unidade.objects.create(
                    nome=f'{municipio} - {nome_unidade}', status='Mobilizado')
                unidade.empresasecundaria.set(times)

                if nome_unidade == 'Sede':
                    bairros_unidade = bairros
                    base_lat, base_lon = lat, lon
                else:
                    bairros_unidade = [f'Centro de {nome_unidade}',
                                       f'Zona Rural de {nome_unidade}']
                    base_lat, base_lon = self.jitter(lat, 0.12), self.jitter(lon, 0.12)

                for bairro in bairros_unidade:
                    b_lat, b_lon = self.jitter(base_lat, 0.02), self.jitter(base_lon, 0.02)
                    loc_j = LocalidadeJardiangem.objects.create(
                        nome=bairro, lat_med=b_lat, long_med=b_lon, unidade=unidade)
                    loc_l = LocalidadeLimpezaPredial.objects.create(
                        nome=bairro, lat_med=b_lat, long_med=b_lon, unidade=unidade)

                    for _ in range(rng.randint(2, 3)):
                        t = rng.choice(times_j)
                        servicos, vegetacoes, terrenos = recursos[t.pk]
                        tipo, dmin, dmax = rng.choice(TIPOS_AREA_JARDINAGEM)
                        area = AreasJardins.objects.create(
                            nome=f'{tipo} {rng.choice(NOMES_PROPRIOS)}'[:100],
                            dimensao=round(rng.uniform(dmin, dmax), 1),
                            Terreno=rng.choice(terrenos),
                            vegetacao=rng.choice(vegetacoes),
                            servico=rng.choice(servicos),
                            localidade=loc_j,
                            periodicidade=rng.choice(PERIODICIDADES),
                        )
                        area.time = t
                        self.areas_j.append(area)

                    for _ in range(rng.randint(1, 2)):
                        t = rng.choice(times_l)
                        tipo, dmin, dmax = rng.choice(TIPOS_AREA_LIMPEZA)
                        area = AreaLimpezaPredial.objects.create(
                            nome=f'{tipo} {rng.choice(NOMES_PROPRIOS)}'[:100],
                            dimensao=round(rng.uniform(dmin, dmax), 1),
                            servico=rng.choice(self.catalogo_l[t.pk]),
                            localidade=loc_l,
                        )
                        area.time = t
                        self.areas_l.append(area)

        self.log(f'{len(self.prefeituras)} prefeituras')
        self.log(f'{sum(len(t) for t in self.times_por_prefeitura.values())} times')
        self.log(f'{len(self.areas_j)} áreas de jardinagem e {len(self.areas_l)} de limpeza predial')

    # ------------------------------------------------------------------
    def novo_gerente(self, username, login):
        gerente = Gerente(
            email=f'{login}@{DOMINIO_EMAIL}',
            username=username,
            status='Mobilizado',
            is_active=True,
            is_admin=True,
            is_staff=True,
            is_superuser=True,
        )
        # senha definida antes do save: o model não tenta enviar e-mail
        gerente.set_password(SENHA_PADRAO)
        gerente.save()
        return gerente

    def criar_gerentes(self):
        self.stdout.write('Criando gerentes...')
        rng = self.rng
        self.gerentes = []
        self.gerentes_por_time = {}

        for username, login, municipios in GERENTES_MULTI:
            gerente = self.novo_gerente(username, login)
            times = [t for m in municipios for t in self.times_por_prefeitura[m]]
            gerente.empresasecundaria.set(times)
            self.gerentes.append(gerente)
            for t in times:
                self.gerentes_por_time.setdefault(t.pk, []).append(gerente)

        # equipe local: 2 pessoas por time (encarregado + colaborador)
        usados = set()
        for municipio, times in self.times_por_prefeitura.items():
            for t in times:
                for _ in range(2):
                    while True:
                        nome = f'{rng.choice(PRIMEIROS_NOMES)} {rng.choice(SOBRENOMES)}'
                        if nome not in usados:
                            usados.add(nome)
                            break
                    login = (nome.lower().replace(' ', '.')
                             .translate(str.maketrans('áéíóúãõâêôç', 'aeiouaoaeoc')))
                    gerente = self.novo_gerente(nome, login)
                    gerente.empresasecundaria.set([t])
                    self.gerentes.append(gerente)
                    self.gerentes_por_time.setdefault(t.pk, []).append(gerente)

        self.log(f'{len(self.gerentes)} gerentes (senha {SENHA_PADRAO})')

    def criar_permissoes_gerentes(self):
        pares = [
            (PermissionsAccessJardinagem, list(PermissionsJardinagem.objects.all())),
            (PermissionsAccessLimpezaPredial, list(PermissionsLimpezaPredial.objects.all())),
            (PermissionsAccessEspecials, list(PermissionsEspecials.objects.all())),
        ]
        for modelo, permissoes in pares:
            if not permissoes:
                continue
            acessos = modelo.objects.bulk_create([modelo(Gerente=g) for g in self.gerentes])
            through = modelo.Permissions.through
            campo_acesso = f'{modelo._meta.model_name}_id'
            campo_perm = f'{permissoes[0]._meta.model_name}_id'
            through.objects.bulk_create([
                through(**{campo_acesso: a.pk, campo_perm: p.pk})
                for a in acessos for p in permissoes])
        self.log('permissões completas atribuídas a todos os gerentes')

    # ------------------------------------------------------------------
    def sortear_data(self, dias_passado, dias_futuro):
        """Mais peso no presente, para o Kanban ter volume nas colunas por data."""
        rng = self.rng
        faixa = rng.random()
        if faixa < 0.12:
            dias = rng.uniform(-7, 7)
        elif faixa < 0.80:
            dias = -rng.uniform(7, dias_passado)
        else:
            dias = rng.uniform(7, dias_futuro)
        dia = (self.agora + timedelta(days=dias)).date()
        return timezone.make_aware(datetime.combine(dia, rng.choice(HORARIOS)))

    def sortear_status(self, inicio):
        rng = self.rng
        dias = (inicio - self.agora).total_seconds() / 86400
        sorteio = rng.random()
        if dias > 1:                       # futuro
            return 'Cancelado' if sorteio < 0.04 else 'Agendado'
        if dias > -3:                      # hoje e últimos dias
            if sorteio < 0.35:
                return 'Em andamento'
            if sorteio < 0.65:
                return 'Concluido'
            return 'Agendado'
        if sorteio < 0.84:                 # passado: histórico
            return 'Concluido'
        if sorteio < 0.90:
            return 'Cancelado'
        return 'Agendado'                  # atrasado

    def criar_servicos(self, opts):
        self.stdout.write('Criando serviços, acompanhamentos e checklists...')
        dias_passado = opts['meses_historico'] * 30
        dias_futuro = opts['meses_futuro'] * 30
        media = opts['servicos_por_area']
        self.total = {}

        self._servicos_jardinagem(media, dias_passado, dias_futuro)
        self._servicos_limpeza(media, dias_passado, dias_futuro)

    def _datas(self, servico, status):
        rng = self.rng
        conclusao = None
        if status == 'Concluido':
            conclusao = servico + timedelta(hours=rng.uniform(1, 6))
        return conclusao

    def _servicos_jardinagem(self, media, dias_passado, dias_futuro):
        rng = self.rng
        tipos = ['Regular'] * 7 + ['Extra', 'Automático']
        agendados, meta = [], []

        configurados = []
        for area in self.areas_j:
            configurados.append(ServicoJardinagemConfigurado(
                Areas=area, horario_1=rng.choice(HORARIOS),
                tempomedioplanejado=timedelta(minutes=rng.choice([30, 60, 90, 120]))))
        configurados = ServicoJardinagemConfigurado.objects.bulk_create(configurados)
        self._m2m_config(ServicoJardinagemConfigurado, configurados,
                         [[a.servico] for a in self.areas_j])

        for area, config in zip(self.areas_j, configurados):
            servicos_time = self.catalogo_j[area.time.pk]
            equipe = self.gerentes_por_time.get(area.time.pk, [])
            for _ in range(max(1, int(rng.gauss(media, media * 0.3)))):
                inicio = self.sortear_data(dias_passado, dias_futuro)
                status = self.sortear_status(inicio)
                escalados = [area.servico] + rng.sample(servicos_time, rng.randint(0, 2))
                agendados.append(ServicoJardinagemAgendado(
                    id_configuracao=config.id_random,
                    DataDeInicio=inicio,
                    DataDeConclusao=self._datas(inicio, status),
                    DescricaoDoServico=f'{escalados[0].nome} — {area.nome}',
                    Areas=area,
                    status=status,
                    TipoServico=rng.choice(tipos),
                    ServicoCompunsivo=rng.random() < 0.05,
                ))
                meta.append((list({s.pk: s for s in escalados}.values()), equipe))

        agendados = ServicoJardinagemAgendado.objects.bulk_create(agendados, batch_size=1000)

        through_serv = ServicoJardinagemAgendado.ServicosEscalados.through
        through_esc = ServicoJardinagemAgendado.ColaboradoresEscalados.through
        through_conf = ServicoJardinagemAgendado.ColaboradoresConfirmados.through
        through_neg = ServicoJardinagemAgendado.ColaboradoresNegados.through
        serv_rows, esc_rows, conf_rows, neg_rows, fatos, checks = [], [], [], [], [], []

        for servico, (escalados, equipe) in zip(agendados, meta):
            for s in escalados:
                serv_rows.append(through_serv(
                    servicojardinagemagendado_id=servico.pk,
                    catalogodeservicojardinagem_id=s.pk))

            pessoas = rng.sample(equipe, min(len(equipe), rng.randint(1, 3))) if equipe else []
            for p in pessoas:
                esc_rows.append(through_esc(servicojardinagemagendado_id=servico.pk, gerente_id=p.pk))
                if servico.status in ('Concluido', 'Em andamento') or rng.random() < 0.6:
                    conf_rows.append(through_conf(servicojardinagemagendado_id=servico.pk, gerente_id=p.pk))
                elif rng.random() < 0.3:
                    neg_rows.append(through_neg(servicojardinagemagendado_id=servico.pk, gerente_id=p.pk))

            fatos += self._acompanhamentos(FatoServicoJardinagem, servico, pessoas)
            chave = next((k for k in CHECKLIST_JARDINAGEM if escalados[0].nome.startswith(k)), 'default')
            checks += self._checklist(CheckListJardinagem, servico, CHECKLIST_JARDINAGEM[chave])

        for modelo, linhas in [(through_serv, serv_rows), (through_esc, esc_rows),
                               (through_conf, conf_rows), (through_neg, neg_rows)]:
            modelo.objects.bulk_create(linhas, batch_size=2000)
        FatoServicoJardinagem.objects.bulk_create(fatos, batch_size=2000)
        CheckListJardinagem.objects.bulk_create(checks, batch_size=2000)

        self.total['jardinagem'] = (len(agendados), len(fatos), len(checks))
        self.log(f'jardinagem: {len(agendados)} serviços, {len(fatos)} acompanhamentos, '
                 f'{len(checks)} itens de checklist')

    def _servicos_limpeza(self, media, dias_passado, dias_futuro):
        rng = self.rng
        tipos = ['Regular'] * 7 + ['Extra', 'Automático']
        agendados, meta = [], []

        configurados = ServicoLimpezaPredialConfigurado.objects.bulk_create([
            ServicoLimpezaPredialConfigurado(
                Areas=area, horario_1=rng.choice(HORARIOS),
                tempomedioplanejado=timedelta(minutes=rng.choice([30, 60, 90])))
            for area in self.areas_l])
        self._m2m_config(ServicoLimpezaPredialConfigurado, configurados,
                         [[a.servico] for a in self.areas_l])

        for area, config in zip(self.areas_l, configurados):
            servicos_time = self.catalogo_l[area.time.pk]
            equipe = self.gerentes_por_time.get(area.time.pk, [])
            for _ in range(max(1, int(rng.gauss(media, media * 0.3)))):
                inicio = self.sortear_data(dias_passado, dias_futuro)
                status = self.sortear_status(inicio)
                escalados = [area.servico] + rng.sample(servicos_time, rng.randint(0, 2))
                agendados.append(ServicoLimpezaPredialAgendado(
                    id_configuracao=config.id_random,
                    DataDeInicio=inicio,
                    DataDeConclusao=self._datas(inicio, status),
                    DescricaoDoServico=f'{escalados[0].nome} — {area.nome}',
                    Areas=area,
                    status=status,
                    TipoServico=rng.choice(tipos),
                ))
                meta.append((list({s.pk: s for s in escalados}.values()), equipe))

        agendados = ServicoLimpezaPredialAgendado.objects.bulk_create(agendados, batch_size=1000)

        through_serv = ServicoLimpezaPredialAgendado.ServicosEscalados.through
        serv_rows, fatos, checks = [], [], []
        for servico, (escalados, equipe) in zip(agendados, meta):
            for s in escalados:
                serv_rows.append(through_serv(
                    servicolimpezapredialagendado_id=servico.pk,
                    catalogodeservicolimpezapredial_id=s.pk))
            pessoas = rng.sample(equipe, min(len(equipe), rng.randint(1, 2))) if equipe else []
            fatos += self._acompanhamentos(FatoServicoLimpezaPredial, servico, pessoas)
            checks += self._checklist(CheckListLimpezaPredial, servico, CHECKLIST_LIMPEZA)

        through_serv.objects.bulk_create(serv_rows, batch_size=2000)
        FatoServicoLimpezaPredial.objects.bulk_create(fatos, batch_size=2000)
        CheckListLimpezaPredial.objects.bulk_create(checks, batch_size=2000)

        self.total['limpeza'] = (len(agendados), len(fatos), len(checks))
        self.log(f'limpeza predial: {len(agendados)} serviços, {len(fatos)} acompanhamentos, '
                 f'{len(checks)} itens de checklist')

    def _m2m_config(self, modelo, configurados, servicos):
        """Dias da semana e serviços escalados das configurações."""
        rng = self.rng
        nome = modelo._meta.model_name
        through_serv = modelo.ServicosEscalados.through
        through_dias = modelo.diasaseremrealizado.through
        campo_serv = [f.name for f in through_serv._meta.fields
                      if f.name not in ('id', nome)][0]
        linhas_serv, linhas_dias = [], []
        for config, lista in zip(configurados, servicos):
            for s in lista:
                linhas_serv.append(through_serv(**{f'{nome}_id': config.pk, f'{campo_serv}_id': s.pk}))
            for dia in rng.sample(self.dias[:6], rng.randint(1, 3)):
                linhas_dias.append(through_dias(**{f'{nome}_id': config.pk, 'diasdasemana_id': dia.pk}))
        through_serv.objects.bulk_create(linhas_serv, batch_size=2000)
        through_dias.objects.bulk_create(linhas_dias, batch_size=2000)

    def _acompanhamentos(self, modelo, servico, pessoas):
        """Registros de chegada/saída da equipe na área (acompanhamento do serviço)."""
        rng = self.rng
        if servico.status not in ('Concluido', 'Em andamento') or not pessoas:
            return []
        registros = []
        for pessoa in pessoas:
            chegada = servico.DataDeInicio + timedelta(minutes=rng.randint(-10, 40))
            if servico.status == 'Concluido' and servico.DataDeConclusao:
                retorno = servico.DataDeConclusao - timedelta(minutes=rng.randint(0, 20))
            else:
                retorno = chegada + timedelta(minutes=rng.randint(20, 90))
            registros.append(modelo(Servico=servico, Gerente=pessoa,
                                    data_hora_chegada_na_area=chegada,
                                    data_hora_retorno_area=max(retorno, chegada)))
        return registros

    def _checklist(self, modelo, servico, itens):
        rng = self.rng
        linhas = []
        for posicao, item in enumerate(itens):
            if servico.status == 'Concluido':
                status = 'Concluído'
            elif servico.status == 'Em andamento':
                status = 'Concluído' if posicao < len(itens) // 2 or rng.random() < 0.3 else 'Pendente'
            else:
                status = 'Pendente'
            linhas.append(modelo(servico_agendado=servico, descricao=item, status=status))
        return linhas

    # ------------------------------------------------------------------
    def resumo(self):
        self.stdout.write(self.style.SUCCESS('\nCenário de teste criado.'))
        self.stdout.write(f'Login de exemplo: micaelle@{DOMINIO_EMAIL} / {SENHA_PADRAO}')
        self.stdout.write(f'Suporte (todas as prefeituras): suporte@{DOMINIO_EMAIL} / {SENHA_PADRAO}')
        self.stdout.write('Para remover: python manage.py popular_cenario_teste --apagar')
