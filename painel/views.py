from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from automacoes.executor import esta_pendente, executar
from automacoes.models import Execucao, Rotina
from notificacoes_email.envios import enviar_teste
from notificacoes_email.models import NotificacaoEnviada


def _time_interno(user):
    return user.is_authenticated and user.is_active and (user.is_superuser or user.is_staff)


interno = user_passes_test(_time_interno, login_url='painel:login')


class Login(auth_views.LoginView):
    template_name = 'painel/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not _time_interno(form.get_user()):
            messages.error(self.request, 'Acesso exclusivo para os times internos (superusuários ou equipe).')
            return redirect('painel:login')
        return super().form_valid(form)


def sair(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('painel:login')


@interno
def inicio(request):
    hoje = timezone.localdate()
    rotinas = list(Rotina.objects.all())
    for r in rotinas:
        r.pendente = esta_pendente(r)
        r.ultima = r.ultima_execucao
        r.hoje_ok = r.execucoes.filter(data_referencia=hoje, status='sucesso').exists()

    ultimos_dias = [hoje - timedelta(days=i) for i in range(6, -1, -1)]
    serie = []
    for d in ultimos_dias:
        agg = Execucao.objects.filter(data_referencia=d).aggregate(
            ok=Count('id', filter=Q(status='sucesso')), erro=Count('id', filter=Q(status='erro')),
        )
        emails = NotificacaoEnviada.objects.filter(criada_em__date=d, status='enviado').count()
        serie.append({'dia': d, 'ok': agg['ok'], 'erro': agg['erro'], 'emails': emails})
    maior = max([s['emails'] for s in serie] + [1])
    for s in serie:
        s['altura'] = max(4, int(s['emails'] / maior * 100))

    contexto = {
        'secao': 'inicio',
        'rotinas': rotinas,
        'serie': serie,
        'kpi_execucoes_hoje': Execucao.objects.filter(iniciada_em__date=hoje).count(),
        'kpi_erros_7d': Execucao.objects.filter(status='erro', iniciada_em__date__gte=hoje - timedelta(days=7)).count(),
        'kpi_emails_hoje': NotificacaoEnviada.objects.filter(criada_em__date=hoje, status='enviado').count(),
        'kpi_falhas_email': NotificacaoEnviada.objects.filter(status='falhou').count(),
        'ultimas': Execucao.objects.select_related('rotina')[:8],
    }
    return render(request, 'painel/inicio.html', contexto)


@interno
def rotinas(request):
    lista = list(Rotina.objects.all())
    for r in lista:
        r.pendente = esta_pendente(r)
        r.ultima = r.ultima_execucao
    return render(request, 'painel/rotinas.html', {'secao': 'rotinas', 'rotinas': lista, 'hoje': timezone.localdate()})


@interno
@require_POST
def alternar_rotina(request, pk):
    rotina = get_object_or_404(Rotina, pk=pk)
    rotina.ativa = not rotina.ativa
    rotina.save(update_fields=['ativa', 'atualizada_em'])
    messages.success(request, f'{rotina.nome}: {"ativada" if rotina.ativa else "pausada"}.')
    return redirect('painel:rotinas')


@interno
@require_POST
def horario_rotina(request, pk):
    rotina = get_object_or_404(Rotina, pk=pk)
    try:
        h, m = request.POST.get('horario', '').split(':')[:2]
        rotina.horario = timezone.datetime.strptime(f'{h}:{m}', '%H:%M').time()
        rotina.save(update_fields=['horario', 'atualizada_em'])
        messages.success(request, f'{rotina.nome}: novo horário {rotina.horario:%H:%M}.')
    except ValueError:
        messages.error(request, 'Horário inválido.')
    return redirect('painel:rotinas')


@interno
@require_POST
def executar_rotina(request, pk):
    rotina = get_object_or_404(Rotina, pk=pk)
    try:
        data = date.fromisoformat(request.POST.get('data') or timezone.localdate().isoformat())
    except ValueError:
        messages.error(request, 'Data inválida.')
        return redirect('painel:rotinas')
    execucao = executar(rotina, data=data, origem='manual', usuario=request.user.email)
    if execucao is None:
        messages.warning(request, 'Esta rotina já está rodando agora. Aguarde alguns segundos.')
    elif execucao.status == 'sucesso':
        messages.success(request, f'{rotina.nome}: {execucao.itens_criados} criado(s), {execucao.itens_ignorados} ignorado(s).')
    else:
        messages.error(request, f'{rotina.nome} falhou. Veja os detalhes da execução.')
    return redirect(request.POST.get('voltar') or 'painel:rotinas')


@interno
def execucoes(request):
    qs = Execucao.objects.select_related('rotina')
    if request.GET.get('rotina'):
        qs = qs.filter(rotina__codigo=request.GET['rotina'])
    if request.GET.get('status'):
        qs = qs.filter(status=request.GET['status'])
    pagina = Paginator(qs, 25).get_page(request.GET.get('pagina'))
    return render(request, 'painel/execucoes.html', {
        'secao': 'execucoes', 'pagina': pagina, 'rotinas': Rotina.objects.all(), 'status_opcoes': Execucao.STATUS,
    })


@interno
def execucao_detalhe(request, pk):
    execucao = get_object_or_404(Execucao.objects.select_related('rotina'), pk=pk)
    return render(request, 'painel/execucao_detalhe.html', {'secao': 'execucoes', 'e': execucao})


@interno
def notificacoes(request):
    qs = NotificacaoEnviada.objects.all()
    if request.GET.get('tipo'):
        qs = qs.filter(tipo=request.GET['tipo'])
    if request.GET.get('status'):
        qs = qs.filter(status=request.GET['status'])
    if request.GET.get('busca'):
        qs = qs.filter(Q(email__icontains=request.GET['busca']) | Q(assunto__icontains=request.GET['busca']))
    pagina = Paginator(qs, 30).get_page(request.GET.get('pagina'))
    return render(request, 'painel/notificacoes.html', {
        'secao': 'notificacoes', 'pagina': pagina,
        'tipos': NotificacaoEnviada.TIPOS, 'status_opcoes': NotificacaoEnviada.STATUS,
    })


@interno
def configuracoes(request):
    from django.conf import settings
    if request.method == 'POST':
        email = request.POST.get('email') or request.user.email
        if enviar_teste(email, request.user.username):
            messages.success(request, f'E-mail de teste enviado para {email}.')
        else:
            messages.error(request, 'Não foi possível enviar. Veja o erro na lista de notificações.')
        return redirect('painel:configuracoes')
    return render(request, 'painel/configuracoes.html', {
        'secao': 'configuracoes',
        'email_host': settings.EMAIL_HOST, 'email_port': settings.EMAIL_PORT,
        'email_user': settings.EMAIL_HOST_USER, 'envio_real': settings.EMAIL_ENVIO_REAL,
        'tls': settings.EMAIL_USE_TLS, 'ssl': settings.EMAIL_USE_SSL,
        'zeladorx_url': settings.ZELADORX_URL,
    })
