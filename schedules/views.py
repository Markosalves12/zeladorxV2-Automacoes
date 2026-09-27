from django.shortcuts import render
from schedules.management.comands.run_scheduled_task_limpeza_predial import agendar_servicos_limpeza_predial_configurados
from schedules.management.comands.run_scheduled_task_jardinagem import agendar_servicos_jardinagem_configurados
import schedule
import time
import threading
from threading import Event
from datetime import datetime

# Evento para sinalizar parada da thread
stop_event = Event()


def iniciar_schedule():
    # Adiciona os agendamentos
    schedule.every().day.at('00:15').do(agendar_servicos_limpeza_predial_configurados)
    schedule.every().day.at('00:15').do(agendar_servicos_jardinagem_configurados)

    while not stop_event.is_set():
        # Obtém o próximo agendamento
        next_run = schedule.next_run()

        if next_run:
            # Calcula o tempo até o próximo agendamento em segundos
            now = datetime.now()
            sleep_time = (next_run - now).total_seconds()

            # Garante que o sleep não seja negativo (caso o horário já tenha passado)
            if sleep_time < 0:
                sleep_time = 60  # Verifica novamente em 1 minuto se o horário passou

            # Dorme até próximo do agendamento, com um buffer de segurança
            max_sleep = 3 * 60 * 60  # 3 horas em segundos
            sleep_time = min(sleep_time - 30, max_sleep)  # Dorme até 30s antes ou 3h no máximo

            if sleep_time > 0:
                time.sleep(sleep_time)

        # Executa tarefas pendentes
        schedule.run_pending()

        # Após executar, verifica novamente em até 3 horas
        if not stop_event.is_set():
            time.sleep(min(60, 3 * 60 * 60))  # Dorme 1 min ou até 3h se nada estiver pendente


# Variável global para a thread
schedule_thread = None


# View para forçar atualizações e reiniciar o schedule
def force_updates(request):
    global schedule_thread

    # Limpa os agendamentos anteriores
    schedule.clear()

    # Para a thread existente, se houver
    if schedule_thread and schedule_thread.is_alive():
        stop_event.set()  # Sinaliza para a thread parar
        schedule_thread.join(timeout=5)  # Aguarda a thread terminar com timeout
        stop_event.clear()  # Reseta o evento para a próxima thread
        schedule_thread = None  # Remove a referência à thread antiga

    # Inicia uma nova thread para o agendamento
    schedule_thread = threading.Thread(target=iniciar_schedule)
    schedule_thread.daemon = True  # Thread daemon para encerrar com o programa principal
    schedule_thread.start()

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )