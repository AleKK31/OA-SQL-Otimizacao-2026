# Otimização de Consultas com PostgreSQL

**Objeto de Aprendizagem** · OPT016 · UTFPR-CM · Abordagem IMA–CID

**Autor:** Alexandre Borges Baccarini Júnior — RA: 2515520 · Grupo: J

---

## Sobre o OA

Este OA (Objeto de Aprendizagem) ensina **otimização de consultas SQL no PostgreSQL**, que estrutura o conteúdo em três modelos:

- **Conceitual** — o que ensinar
- **Instrucional** — com o que ensinar
- **Didático** — como e em que ordem

**Público-alvo:** Estudantes e profissionais com conhecimento básico de SQL que desejam entender e aplicar técnicas de otimização no PostgreSQL.

---

## Como usar

**Abra `index.html` no navegador para começar. Nenhuma instalação necessária para M1, M2, M3A e M3B.**

```
oa-postgresql/
└── index.html   ← Abra este arquivo no Chrome ou Firefox
```

Para os módulos M3C e a Query 5 da Avaliação Final, é necessário o Docker. Veja [Ambiente Docker](#ambiente-docker).

---

## Módulos

| Módulo | Bloom | Duração | Ambiente |
|--------|-------|---------|----------|
| M1 — Entendendo o Problema | Lembrar + Compreender | ~30 min | Navegador |
| M2 — Diagnóstico | Compreender + Analisar | ~40 min | PGLite (navegador) |
| M3A — Índices | Analisar | ~25 min | PGLite (navegador) |
| M3B — Reescrita de Consulta | Aplicar | ~25 min | PGLite (navegador) |
| M3C — Infraestrutura e Manutenção | Compreender | ~20 min | Docker |
| Avaliação Final | Avaliar | ~20 min | PGLite + Docker (Q5) |

**Especificação aberta (DD):** Você pode navegar pelos módulos na ordem que preferir. A Avaliação Final é liberada após completar todos os módulos M1 a M3C.

---

## Ambiente PGLite

Os módulos M2, M3A, M3B e as Queries 1–4 da AF usam **PGLite** — PostgreSQL em WebAssembly que roda diretamente no navegador, sem instalação. Basta abrir `index.html`.

- Cada editor SQL tem seed próprio (tabelas `clientes` e `pedidos` com ~50k linhas)
- Os seeds **não criam índices** em `cliente_id`, `status` ou `criado_em` — os exercícios dependem disso para demonstrar Seq Scan
- Funciona nos navegadores modernos: Chrome 110+, Firefox 110+, Edge 110+

---

## Ambiente Docker

Necessário para: **M3C** (VACUUM e estatísticas reais) e **Query 5 da AF** (tabela com tuplas mortas).

Instruções completas: [`docker/README.md`](./docker/README.md)

```bash
# Subir o banco
cd docker/
docker compose up -d

# Conectar
psql -h localhost -U oa_user -d oa_db
# Senha: oa_pass
```

Tabelas disponíveis após o seed (~2–3 min):
- `clientes` — 50.000 linhas
- `produtos` — 10.000 linhas
- `pedidos` — 500.000 linhas (sem índices secundários)
- `pedidos_arquivo` — ~100.000 ativas + ~400.000 tuplas mortas (autovacuum desabilitado)

---

## Tecnologias

- HTML
- CSS
- JavaScript
- PGLite
- PostgreSQL
- Docker

