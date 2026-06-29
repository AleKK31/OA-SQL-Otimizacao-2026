# Ambiente Docker — OA de Otimização de Queries PostgreSQL

## Pré-requisitos

- Docker Desktop instalado (<https://www.docker.com/products/docker-desktop/>)
- Porta 5432 disponível

## Subir o banco

```bash
cd docker/
docker compose up -d
```

Aguarde **~2 a 3 minutos** para o seed popular as tabelas (500 mil linhas em `pedidos`).

## Conectar ao banco

**Via psql (linha de comando):**

```bash
psql -h localhost -U oa_user -d oa_db
# Senha: oa_pass
```

**Via DBeaver ou pgAdmin:**

| Campo  | Valor     |
|--------|-----------|
| Host   | localhost |
| Porta  | 5432      |
| Banco  | oa_db     |
| Usuário | oa_user  |
| Senha  | oa_pass   |

## Verificar se o seed completou

```sql
SELECT relname, n_live_tup
FROM pg_stat_user_tables
WHERE relname IN ('clientes', 'produtos', 'pedidos', 'pedidos_arquivo')
ORDER BY relname;
```

Esperado após o seed:

| Tabela           | n_live_tup |
|------------------|-----------|
| clientes         | ≈ 50 000  |
| pedidos          | ≈ 500 000 |
| pedidos_arquivo  | ≈ 100 000 |
| produtos         | ≈ 10 000  |

## Tabelas disponíveis

| Tabela           | Linhas aprox. | Usado em                          |
|------------------|---------------|-----------------------------------|
| `clientes`       | 50 000        | M2, M3A, M3B, AF                  |
| `produtos`       | 10 000        | M2                                |
| `pedidos`        | 500 000       | Todos os módulos                  |
| `pedidos_arquivo`| ~100 000 ativas + ~400 000 tuplas mortas | M3C, AF Query 5 |

> **Atenção:** `pedidos_arquivo` tem `autovacuum_enabled = false` e estatísticas desatualizadas propositalmente. Os exercícios do M3C e da AF dependem disso.

## pg_stat_statements

A extensão já está ativa. Para ver as queries mais lentas:

```sql
SELECT
  LEFT(query, 80) AS query_preview,
  calls,
  round(total_exec_time::numeric, 2) AS total_ms,
  round(mean_exec_time::numeric, 2) AS media_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

## Parar o banco

```bash
docker compose down
```

## Resetar (apagar tudo e recriar)

```bash
docker compose down -v
docker compose up -d
```
