from django.shortcuts import render, redirect
from authenticate.forms import LoginForms, EmailReset, UpdatePassword
from gerente.models import Gerente
from django.contrib import messages
from notifications.utils import enviar_notificacao
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        request.session['login_nome'] = user.username
        request.session['userid'] = user.id_random
        return redirect('calendario_jardinagem', user.id_random)

    if request.POST:
        form = LoginForms(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['senha']
            user = authenticate(email=email, password=password)

            print(user)

            if user:
                login(request, user)
                request.session['login_nome'] = user.username
                request.session['userid'] = user.id_random
                return redirect('calendario_jardinagem', user.id_random)

    else:
        form = LoginForms()

    context['login_form'] = form
    return render(
        request,
        'authenticate/login.html',
        context={
            'forms': LoginForms
        }
    )



def logout_view(request):
    logout(request)
    messages.success(request, "Logout efetuado com sucesso")

    return redirect('login')


def reset_password(request):
    forms = EmailReset()
    if request.method == "POST":
        forms = EmailReset(request.POST)
        if forms.is_valid():
            email = forms['email'].value()

            try:
                gerente = Gerente.objects.get(
                    email=email
                )

                # Gera um token de redefinição de senha e um token para a URL
                reset_token = get_random_string(9)  # Token único de 32 caracteres
                url_token = get_random_string(16)  # Token adicional para URL
                token_expiration = now() + timedelta(hours=1)  # Expira em 1 hora

                # Armazena o token de redefinição e o token de URL na sessão
                request.session['reset_token'] = reset_token
                request.session['url_token'] = url_token
                request.session['token_expiration'] = token_expiration.isoformat()
                request.session['email'] = email

                enviar_notificacao(
                    destinatario=[email],
                    assunto="Alteração de senha",
                    contexto={
                        'username': gerente.username,
                        'email': gerente.email,
                        'randon_token': reset_token
                    },
                    template='notifications/reset_password.html'
                )

                messages.success(request, "Token de troca enviado por email")

                return redirect('update_password', url_token)

            except:
                pass

    return render(
        request=request,
        template_name='authenticate/send_token.html',
        context={
            'forms': forms
        }
    )

def update_password(request, token):
    # Verifica se o token da URL é o mesmo que foi armazenado na sessão
    session_token = request.session.get('reset_token')
    session_token_expiration_str = request.session.get('token_expiration')

    forms = UpdatePassword()

    if request.method == "POST":
        forms = UpdatePassword(request.POST)

        if forms.is_valid():
            email = forms['email'].value()
            token = forms['token'].value()
            new_password = forms['new_password'].value()
            confirm_password = forms['confirm_password'].value()


            # Valida se o token da URL e o token da sessão são os mesmos
            if token != session_token:
                messages.error(request, "Token inválido. Solicite outro.")
                return redirect('reset_password')  # Redireciona para a página de solicitação de token

            # Valida se o token expirou
            if session_token_expiration_str:
                # Converte a string de data de expiração para um objeto datetime
                session_token_expiration = datetime.fromisoformat(session_token_expiration_str)
                if now() > session_token_expiration:
                    messages.error(request, "Token expirado. Solicite outro.")
                    return redirect('reset_password')  # Redireciona para a página de solicitação de token

            try:
                gerente = Gerente.objects.get(
                    email=email
                )

                if new_password != confirm_password:
                    messages.error(request, "Senhas devem ser iguais")


                else:
                    # Atualizar as senhas
                    gerente.set_password(new_password)
                    gerente.reset_token = None  # Invalida o token após o uso
                    gerente.token_expiration = None
                    gerente.save()

                    messages.success(request, "Senhas alterada com sucesso")

                    # Redirecionar para uma página de sucesso
                    return redirect('login')

            except:
                pass


    return render(
        request=request,
        template_name='authenticate/reset_password.html',
        context={
            'forms': forms,
            'token': token
        }
    )