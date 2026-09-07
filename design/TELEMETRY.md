# Telemetria automática — Horizonte

A automação atualiza somente `assets/horizonte/telemetry.json`, `telemetry.svg` e `telemetry-mobile.svg`. O README e as demais peças não são modificados. O gerador visual existente foi mantido: mesmas dimensões, textos, paleta, tipografia e layout desktop/mobile.

| Métrica | Fonte e cálculo |
| --- | --- |
| Repositórios públicos | `GET /users/FernandoHenriqueCampos/repos?type=owner&per_page=100&page=N`: quantidade de repositórios públicos pertencentes ao usuário, incluindo forks. |
| Repositórios originais | Mesma listagem, filtrada por `fork == false`. “Original” significa sem fork, não uma afirmação de autoria exclusiva. |
| Estrelas recebidas | Soma de `stargazers_count` nos repositórios públicos sem forks. |

A paginação é percorrida até o fim. `GET /users/FernandoHenriqueCampos`, campo `public_repos`, confere se a listagem está completa. Duplicatas, resposta inválida, falha de rede ou mudança de quantidade durante a coleta interrompem a execução sem publicar zeros ou dados parciais. As fontes e os registros usados no cálculo ficam no JSON.

**Frequência:** diariamente às **08:23 UTC / 05:23 em São Paulo**, além de **Actions → Update Horizonte telemetry → Run workflow**, usando a branch principal. O agendador do GitHub pode atrasar execuções. Não há execução por push ou por pull request.

**Sem commits vazios:** o script compara os dados e os registros dos repositórios, ignorando horário da coleta e ordem da resposta. Se nada mudou, não escreve nenhum arquivo. A data exibida continua sendo a coleta que produziu o snapshot publicado; a última verificação pode ser consultada no histórico do Actions. Criação, remoção, renomeação, mudança de status de fork ou de estrelas são mudanças reais, mesmo se os totais coincidirem.

**Permissões:** `permissions: {}` no workflow e somente `contents: write` no job, necessária para enviar os três arquivos atualizados. Usa o `GITHUB_TOKEN` temporário do próprio GitHub, sem PAT ou segredo adicional. O checkout oficial é fixado por SHA. O push não usa force; concorrência é serializada e uma atualização conflitante falha sem sobrescrever commits de terceiros.

**Execução local:** `python design/update_telemetry.py`. `GITHUB_TOKEN` é opcional fora do Actions. Para reproduzir o visual usando o JSON salvo, sem consultar a rede: `python design/update_telemetry.py --from-snapshot`.

**Testes:** `python -m unittest discover -s design -p "test_telemetry.py"`.

Referências: [API de repositórios](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user), [agendamento e execução manual](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows). O GitHub pode desativar agendamentos de repositórios públicos após 60 dias sem atividade; nesse caso, reative pelo Actions. A automação não cria commits artificiais para contornar essa regra.
