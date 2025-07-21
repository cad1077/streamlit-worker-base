import sys
import os
import logging
import requests
import time
import schedule

# Adiciona o diretório .local/bin ao PATH do Python
user_bin_path = os.path.expanduser('~/.local/bin')
if user_bin_path not in sys.path:
    sys.path.append(user_bin_path)

LOG_FILE = '/home/cleberdev/orchestrator.log'  # Substitua pelo caminho e nome de arquivo desejados

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

worker_endpoints = [
    "https://app-worker-base-rrzfbjrk8ckdvvso2jzbij.streamlit.app/run-task", # SUA URL DO WORKER
    "https://app-worker-copy-1-aavvcszquxvruugjzrddxh.streamlit.app/run-task",
    # Você adicionará mais URLs de outros workers aqui posteriormente
]

def send_task(endpoint, data):
    try:
        response = requests.post(endpoint, json=data, timeout=10) # Adiciona um timeout
        response.raise_for_status() # Lança uma exceção para códigos de status de erro
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao comunicar com {endpoint}: {e}")
        return None

def monitor_health():
    for endpoint in worker_endpoints:
        try:
            response = requests.get(endpoint, timeout=5) # Ping simples
            if response.status_code == 200:
                logging.info(f"Worker {endpoint} está ativo.")
            else:
                logging.warning(f"Alerta: Worker {endpoint} retornou status {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao pingar {endpoint}: {e}")

def run_orchestration():
    task_data = {"numbers": [5, 6, 7]} # Exemplo de dados de tarefa

    results = []
    for endpoint in worker_endpoints:
        result = send_task(endpoint, task_data)
        if result:
            results.append(result)

    logging.info(f"Resultados: {results}")
    logging.info("---")

def keep_workers_alive():
    for endpoint in worker_endpoints:
        try:
            requests.get(endpoint, timeout=5)
            logging.info(f"Ping enviado para {endpoint}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao pingar {endpoint} para manter ativo: {e}")

# Agendamento para manter os workers ativos (ping a cada 45 minutos)
schedule.every(45).minutes.do(keep_workers_alive)

# Agendamento para executar a orquestração (você pode ajustar a frequência)
schedule.every(1).minute.do(run_orchestration) # Executa a cada minuto para demonstração

# if __name__ == "__main__":
#     logging.info("Orquestrador iniciado.")
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
