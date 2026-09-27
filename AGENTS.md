# AGENTS.md — zeladorxV2-Automacoes

- Apps compartilhados (areas, servicos, gerente, unidade, ...) são cópias do zeladorxV2: nunca editar nem criar migrações neles, porque o banco é o mesmo do app principal.
- Somente automacoes, notificacoes_email e painel têm código e migrações próprios; o release do Heroku migra apenas esses apps.
- Toda automação passa por automacoes.executor (trava por linha + registro de Execucao) para rodar uma vez por dia e sobreviver a falhas.
- Geração de serviços é idempotente (id_configuracao + DataDeInicio) e e-mails usam chave única em NotificacaoEnviada, para reprocessar sem duplicar.
- Senhas, convites e códigos de troca de senha ficam no app principal; aqui só e-mails operacionais.
- Localmente os e-mails vão para o terminal (EMAIL_ENVIO_REAL=False) para não disparar aos gerentes de teste.
- Visual replica os tokens e proporções do zeladorxV2 (azul sólido, superfícies claras, raio de 8 px, Sora/Manrope e sidebar recolhível) para manter continuidade entre plataformas.
