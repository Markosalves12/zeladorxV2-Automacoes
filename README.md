# ZeladorX Automações

Plataforma **interna** da família ZeladorX (uso dos times da empresa, não dos clientes). Cuida de tudo que roda sozinho:

- **Geração dos serviços automáticos** de Jardinagem e Limpeza Predial a partir das configurações — substitui a chamada diária à rota `force_updates/` e a thread que podia morrer.
- **E-mails operacionais**: resumo diário, alerta de serviços atrasados e resumo de serviços concluídos.
- **Painel** com rotinas, histórico de execuções, e-mails enviados e teste de envio.

## Família ZeladorX

| Repositório | Papel |
|---|---|
| zeladorxV2 | App principal (clientes) — mantém suas rotas, inclusive `force_updates/` |
| CHATCHANNELS | Chat |
| zeladorxV2APIs-Jardinagem | APIs |
| ZeladorX-institucional | Site |
| **zeladorxV2-Automacoes** | Automações e notificações (interno) |

Mesmo banco, mesma `SECRET_KEY` e mesmo cookie `sessionid` → login compartilhado. Acesso só para superusuários ou equipe (`is_staff`).

## Apps

- **Compartilhados** (cópia do zeladorxV2, não editar): areas, servicos, gerente, unidade, localidade, empresas, catálogo etc.
- **Exclusivos**: `automacoes` (rotinas, execuções, gerador), `notificacoes_email` (envios e registro), `painel` (telas).

## Rotinas padrão

| Código | Horário | O que faz |
|---|---|---|
| gerar_jardinagem | 00:15 | Cria serviços automáticos de Jardinagem |
| gerar_limpeza_predial | 00:15 | Cria serviços automáticos de Limpeza Predial |
| email_resumo_diario | 06:30 | Serviços previstos do dia por gerente |
| email_atrasados | 09:00 | Serviços vencidos nos últimos 7 dias |
| email_concluidos | 18:00 | Serviços concluídos no dia |

Cada rotina roda **uma vez por dia**, depois do horário. Se o agendador atrasar ou falhar, a próxima rodada recupera. Nada é criado ou enviado em dobro. Horários, pausa e execução manual (inclusive para datas passadas) ficam no painel.

## Rodando local

```powershell
python -m venv .venv; .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # preencha a senha do banco
python manage.py migrate automacoes
python manage.py migrate notificacoes_email
python manage.py runserver 8001
```

Abra http://127.0.0.1:8001 e entre com um superusuário do ZeladorX.

```powershell
python manage.py executar_automacoes                 # roda o que estiver pendente
python manage.py executar_automacoes --listar
python manage.py executar_automacoes --rotina gerar_jardinagem --data 2026-09-26
```

Localmente os e-mails aparecem no terminal (`EMAIL_ENVIO_REAL=False`) para não disparar aos gerentes de teste.

## Heroku

1. `heroku create zeladorx-automacoes` e `git push heroku main`.
2. Config vars: `DATABASE_URL` (o mesmo do ZeladorX), `SECRET_KEY` (igual), `AMBIENTE=producao`, `EMAIL_*`, `ZELADORX_URL`.
3. `heroku addons:create scheduler:standard` → tarefa `python manage.py executar_automacoes` **a cada 10 minutos**.
4. Depois de conferir as execuções no painel, pare de chamar `force_updates/` às 23:55.

## Não fazer

- Não rodar `makemigrations` nos apps compartilhados.
- Não enviar senhas por aqui — continuam no app principal.
