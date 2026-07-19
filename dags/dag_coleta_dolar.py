from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2

# ---------- Configurações do banco ----------
DB_CONFIG = {
    "host": "postgres_dolar",   # nome do serviço no docker-compose
    "port": 5432,
    "dbname": "dolar_db",
    "user": "postgres",
    "password": "admin"
}

default_args = {
    "owner": "bruno",
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
}

# ---------- Funções ----------
def consultar_e_inserir():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    dados = resp.json()["USDBRL"]

    cotacao = {
        "valor_compra": float(dados["bid"]),
        "valor_venda": float(dados["ask"]),
        "data_hora": datetime.fromtimestamp(int(dados["timestamp"])),
        "fonte": "AwesomeAPI"
    }

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO cotacoes (moeda, valor_compra, valor_venda, data_hora, fonte)
        VALUES (%s, %s, %s, %s, %s)
        """,
        ("USD", cotacao["valor_compra"], cotacao["valor_venda"],
         cotacao["data_hora"], cotacao["fonte"])
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Cotação inserida: {cotacao}")

# ---------- Definição do DAG ----------
with DAG(
    dag_id="dag_coleta_dolar",
    default_args=default_args,
    description="Consulta cotação do dólar a cada 5 minutos e salva no banco",
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2026, 7, 13),
    catchup=False,
    tags=["dolar", "monitoramento"],
) as dag:

    task_consultar_cotacao = PythonOperator(
        task_id="consultar_e_inserir_cotacao",
        python_callable=consultar_e_inserir,
    )

    task_consultar_cotacao
