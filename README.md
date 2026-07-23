# 💵 Monitor de Cotação do Dólar

📄 Licença
Este projeto é de uso pessoal/educacional. Adapte conforme necessário.

Sistema de coleta automatizada, armazenamento e visualização em tempo real da cotação USD/BRL, com dashboard interativo estilo BI.

## 📋 Sobre o Projeto

Este projeto coleta a cotação do dólar em intervalos regulares (a cada 5 minutos), armazena os dados em um banco PostgreSQL e exibe um dashboard interativo com filtros de data, KPIs e gráficos dinâmicos.

## 🏗️ Arquitetura

┌─────────────┐ ┌──────────────┐ ┌─────────────────┐ │ API Câmbio │ ───▶ │ Script de │ ───▶ │ PostgreSQL │ │ (externa) │ │ Coleta (5min)│ │ (Docker) │ └─────────────┘ └──────────────┘ └─────────────────┘ │ ▼ ┌─────────────────┐ │ Dashboard │ │ (Streamlit + │ │ Plotly) │ └─────────────────┘

## 🚀 Tecnologias

- **Python 3.x**
- **PostgreSQL** (via Docker)
- **psycopg2** — conexão com o banco
- **pandas** — manipulação de dados
- **Streamlit** — interface web interativa
- **Plotly** — gráficos interativos
- **Docker / Docker Compose** — orquestração do banco de dados

## 📦 Estrutura do Projeto

dolar-monitor/ ├── docker-compose.yml # Configuração do container Postgres ├── coleta_cotacao.py # Script de coleta periódica (5 em 5 min) ├── app_dashboard.py # Dashboard interativo (Streamlit) ├── requirements.txt # Dependências Python └── README.md

## ⚙️ Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados
- Python 3.9+
- pip

## 🔧 Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd dolar-monitor

pip install -r requirements.txt

## requirements:
psycopg2-binary
pandas
streamlit
plotly
streamlit-autorefresh
requests

## Subir o banco de dados (PostgreSQL via Docker)
docker-compose up -d
docker ps

# Criar a tabela COTACOES
CREATE TABLE cotacoes (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    valor_compra NUMERIC(10, 4) NOT NULL,
    valor_venda NUMERIC(10, 4) NOT NULL,
    fonte VARCHAR(50)
);

▶️ Como Executar
## Iniciar a coleta de dados (roda a cada 5 minutos)

python coleta_cotacao.py


▶️ Iniciar o dashboard

streamlit run app_dashboard.py


📊 O dashboard estará disponível em: http://localhost:8501

📊 Funcionalidades do Dashboard
Filtros de data (período personalizado)
Filtro por fonte de cotação
KPIs: cotação atual, variação %, mínima, máxima, média
Gráfico de linha com evolução de compra/venda (interativo, com zoom e hover)
Gráfico de spread (venda - compra)
Histograma de distribuição dos valores
Tabela de dados brutos exportável
Atualização automática a cada 60 segundos, sincronizada com as novas inserções no banco


🔄 Comandos Úteis do Docker

Comando	Descrição
docker-compose up -d	Sobe o banco em segundo plano
docker-compose down	Para e remove os containers
docker-compose down -v	Para os containers e remove os volumes (apaga os dados)
docker ps	Lista containers em execução
docker logs postgres_dolar	Exibe logs do container do Postgres


🗂️ Configuração do Banco (docker-compose.yml)
Variável	Valor padrão
Host	localhost
Porta	5432
Banco	dolar_db
Usuário	postgres
Senha	admin


🛠️ Roadmap / Melhorias Futuras
 Notificações via LISTEN/NOTIFY (Postgres) para atualização em tempo real
 Deploy do dashboard em ambiente cloud (Streamlit Cloud / Docker)
 Alertas automáticos (e-mail/Telegram) em variações bruscas
 Comparação com outras moedas (EUR, GBP)
 Exportação de relatórios em PDF


Desenvolvido por Bruno 🚀
 