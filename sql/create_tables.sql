CREATE TABLE IF NOT EXISTS cotacoes (
    id SERIAL PRIMARY KEY,
    moeda VARCHAR(10) NOT NULL DEFAULT 'USD',
    valor_compra NUMERIC(10, 4) NOT NULL,
    valor_venda NUMERIC(10, 4) NOT NULL,
    variacao NUMERIC(10, 4),
    data_hora TIMESTAMP NOT NULL DEFAULT NOW(),
    fonte VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_cotacoes_data_hora ON cotacoes(data_hora);