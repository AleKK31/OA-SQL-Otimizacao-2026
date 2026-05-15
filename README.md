# Otimização de Queries com PostgreSQL

> Objeto de Aprendizagem desenvolvido segundo a abordagem **IMA–CID** para a matéria OPT016 - Objetos De Aprendizagem da UTFPR-CM

---

## Público-alvo
 
É direcionado a estudantes e desenvolvedores de software que já possuem conhecimento básico de SQL e desejam evoluir para um nível intermediário/avançado, focando em otimização de consultas no PostgreSQL.
 
| Perfil | Descrição |
|---|---|
| **Formação** | Ciência da Computação, Sistemas de Informação, Engenharia de Software ou áreas relacionadas |
| **Experiência prévia** | Conhecimento básico de SQL (SELECT, WHERE, JOIN, GROUP BY) |
| **Contexto** | Estudantes, profissionais de TI e DBAs em início de carreira |
| **Formato do curso** | Short-course (4 horas) |
 
---
 
## Requisitos de Aprendizagem

Ao concluir este Objeto de Aprendizagem, o estudante será capaz de:

### Diagnóstico e Análise
- [ ] Interpretar a saída do comando `EXPLAIN` e `EXPLAIN ANALYZE`
- [ ] Utilizar `pg_stat_statements` para identificar queries de alto custo
- [ ] Monitorar queries em execução com `pg_stat_activity`
- [ ] Compreender as métricas de custo: tempo, I/O, CPU e memória

### Plano de Execução
- [ ] Identificar os principais nós de um plano de execução (Seq Scan, Index Scan, Hash Join etc.)
- [ ] Diferenciar as estratégias de join (Nested Loop, Hash Join, Merge Join) e suas condições de uso
- [ ] Compreender como o PostgreSQL estima o custo de uma query
- [ ] Entender o impacto do paralelismo no plano de execução

### Índices
- [ ] Diferenciar os tipos de índice do PostgreSQL (B-Tree, GIN, GiST, BRIN, Parcial, Composto, de Expressão)
- [ ] Escolher o tipo de índice adequado para cada situação
- [ ] Aplicar o conceito de índice cobridor (Index Only Scan)
- [ ] Identificar e remover índices não utilizados

### Reescrita de Query
- [ ] Reconhecer antipadrões SQL (SELECT *, OFFSET elevado, N+1, função em coluna do WHERE)
- [ ] Reescrever queries utilizando CTEs, EXISTS e JOINs explícitos de forma eficiente
- [ ] Diferenciar CTE Materializada de CTE Não Materializada
- [ ] Aplicar Materialized Views para resultados pré-computados

### Estatísticas e VACUUM
- [ ] Compreender o papel das estatísticas do planejador (cardinalidade, histograma, MCV)
- [ ] Executar e interpretar `VACUUM` e `ANALYZE`
- [ ] Configurar o `autovacuum` adequadamente

---
 
## Mapa Conceitual
 
[link em breve](url)
 
