-- seed.sql — OA de Otimização de Queries com PostgreSQL
-- Popula as tabelas com dados realistas para todos os exercícios
-- NÃO cria índices secundários em cliente_id, status ou criado_em

-- Extensão de monitoramento
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- TABELAS

-- Clientes (50.000 linhas)
CREATE TABLE clientes (
  id         SERIAL PRIMARY KEY,
  nome       VARCHAR(100),
  email      VARCHAR(150),
  cidade     VARCHAR(80),
  criado_em  TIMESTAMP DEFAULT NOW()
);

-- Produtos (10.000 linhas)
CREATE TABLE produtos (
  id         SERIAL PRIMARY KEY,
  nome       VARCHAR(100),
  categoria  VARCHAR(50),
  preco      NUMERIC(10,2),
  estoque    INTEGER
);

-- Pedidos (500.000 linhas)
-- SEM índice em cliente_id ou status — propositalmente
CREATE TABLE pedidos (
  id          SERIAL PRIMARY KEY,
  cliente_id  INTEGER REFERENCES clientes(id),
  produto_id  INTEGER REFERENCES produtos(id),
  status      VARCHAR(20) DEFAULT 'pendente',
  quantidade  INTEGER,
  total       NUMERIC(10,2),
  criado_em   TIMESTAMP DEFAULT NOW()
);

-- Tabela para exercício do VACUUM (M3C)
-- autovacuum desabilitado intencionalmente para acumular tuplas mortas
CREATE TABLE pedidos_arquivo (LIKE pedidos INCLUDING ALL);
ALTER TABLE pedidos_arquivo SET (autovacuum_enabled = false);

-- POPULANDO CLIENTES (50.000)

INSERT INTO clientes (nome, email, cidade, criado_em)
SELECT
  'Cliente ' || i AS nome,
  'cliente' || i || '@email.com' AS email,
  CASE (i % 10)
    WHEN 0 THEN 'São Paulo'
    WHEN 1 THEN 'Rio de Janeiro'
    WHEN 2 THEN 'Curitiba'
    WHEN 3 THEN 'Belo Horizonte'
    WHEN 4 THEN 'Porto Alegre'
    WHEN 5 THEN 'Salvador'
    WHEN 6 THEN 'Fortaleza'
    WHEN 7 THEN 'Recife'
    WHEN 8 THEN 'Manaus'
    ELSE 'Goiânia'
  END AS cidade,
  NOW() - ((random() * 730)::int || ' days')::interval AS criado_em
FROM generate_series(1, 50000) i;

-- POPULANDO PRODUTOS (10.000)

INSERT INTO produtos (nome, categoria, preco, estoque)
SELECT
  'Produto ' || i AS nome,
  CASE (i % 8)
    WHEN 0 THEN 'Eletrônicos'
    WHEN 1 THEN 'Roupas'
    WHEN 2 THEN 'Livros'
    WHEN 3 THEN 'Alimentos'
    WHEN 4 THEN 'Esportes'
    WHEN 5 THEN 'Móveis'
    WHEN 6 THEN 'Beleza'
    ELSE 'Brinquedos'
  END AS categoria,
  (random() * 999 + 1)::numeric(10,2) AS preco,
  (random() * 500)::int AS estoque
FROM generate_series(1, 10000) i;

-- POPULANDO PEDIDOS (500.000)

INSERT INTO pedidos (cliente_id, produto_id, status, quantidade, total, criado_em)
SELECT
  (random() * 49999 + 1)::int AS cliente_id,
  (random() * 9999 + 1)::int  AS produto_id,
  CASE (i % 3)
    WHEN 0 THEN 'pendente'
    WHEN 1 THEN 'ativo'
    ELSE 'cancelado'
  END AS status,
  (random() * 10 + 1)::int AS quantidade,
  (random() * 2000 + 10)::numeric(10,2) AS total,
  NOW() - ((random() * 365)::int || ' days')::interval AS criado_em
FROM generate_series(1, 500000) i;

-- POPULANDO PEDIDOS_ARQUIVO (para exercício M3C/AF)
-- ~500.000 linhas inicialmente, depois 80% deletadas = ~100.000 restantes
-- Mais ~400.000 tuplas mortas

INSERT INTO pedidos_arquivo (cliente_id, produto_id, status, quantidade, total, criado_em)
SELECT
  (random() * 49999 + 1)::int AS cliente_id,
  (random() * 9999 + 1)::int  AS produto_id,
  CASE (i % 3)
    WHEN 0 THEN 'pendente'
    WHEN 1 THEN 'ativo'
    ELSE 'cancelado'
  END AS status,
  (random() * 10 + 1)::int AS quantidade,
  (random() * 2000 + 10)::numeric(10,2) AS total,
  NOW() - ((random() * 365)::int || ' days')::interval AS criado_em
FROM generate_series(1, 500000) i;

-- Deletar 80% das linhas para criar tuplas mortas (exercício M3C)
-- NÃO rodar VACUUM nem ANALYZE aqui — deixar estatísticas desatualizadas
DELETE FROM pedidos_arquivo WHERE id % 5 != 0;

-- ATUALIZAR ESTATÍSTICAS DAS TABELAS PRINCIPAIS
-- (pedidos_arquivo fica sem ANALYZE propositalmente)

ANALYZE clientes;
ANALYZE produtos;
ANALYZE pedidos;
-- NÃO rodar ANALYZE em pedidos_arquivo — o exercício M3C/AF depende disso
