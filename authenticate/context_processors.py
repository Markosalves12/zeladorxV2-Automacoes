def classicate_login(request):
    nome = request.session.get('login_nome', '')
    userid = request.session.get('userid', '')

    return {
        'nome': nome,
        'userid': userid,
    }