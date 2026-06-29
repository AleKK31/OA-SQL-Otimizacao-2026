Roteiro:
1. Abrir psql: psql -h localhost -U oa_user -d oa_db
2. Rodar query LENTA (sem índice):
  SELECT * FROM pedidos WHERE cliente_id = 42;
  — Mostrar que demora vários segundos
3. Rodar EXPLAIN ANALYZE e apontar Seq Scan e custo alto
4. Criar o índice:
   CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
5. Rodar a query novamente — agora instantânea
6. Rodar EXPLAIN ANALYZE e apontar Index Scan e custo baixo
