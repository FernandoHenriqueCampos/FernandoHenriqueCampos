# Integração — Horizonte

## Resultado

O README foi integrado na ordem aprovada: Hero → Sobre → Trajetória → Tecnologias → Projetos → Atualmente estudando → GitHub Stats → Além do código → Contato.

As dez variantes SVG aprovadas e a foto original não foram modificadas. `integration-baseline.json` registra os hashes anteriores à integração. Além do código é um interlúdio sem numeração, preservando `08 / CONTATO` na peça aprovada.

O texto profissional preserva cargo trainee, graduação, ordem da trajetória, residência integral de seis meses, projeto para empresa parceira, Code Academy, fundamentos, manutenção e decisões técnicas. Mantém **aprox. 90 min → até 10 min**, além da solução interna **em desenvolvimento** para processos, fluxos, responsabilidades, informações e colaboração. O projeto Adote Já e a contribuição de Fernando foram conferidos no [repositório público](https://github.com/FernandoHenriqueCampos/Grupo-React-Native).

## Arquivos

Modificados: `README.md` e `assets/horizonte/ATTRIBUTIONS.md`.

Adicionados: `design/build_sections.py`, `design/update_telemetry.py`, `design/prepare_github_preview.py`, `design/check_integration.py`, `design/integration-baseline.json`, este relatório e `.github/workflows/telemetry.yml`.

Novos assets em `assets/horizonte/`: `about-heading.svg`, `focus.svg`, `projects.svg`, `exploration.svg`, `telemetry.svg`, `beyond.svg` e suas seis versões `-mobile.svg`, além de `telemetry.json` com dados e fontes.

Assets reutilizados sem alteração: `hero.svg`, `journey.svg`, `technologies.svg`, `footer.svg`, suas quatro versões móveis, as duas versões estáticas das tecnologias e `profile.png`.

`design/build_assets.py` continua sendo a fonte dos tokens e das peças aprovadas. A integração importa suas funções sem executar a regeneração dessas peças.

## Apresentação e acessibilidade

- Sem badges, tabelas, typing, divisores Markdown ou widgets externos.
- SVGs locais e autocontidos, com os mesmos tokens, tipografia e margens do sistema aprovado.
- Versões de composição específicas para desktop e celular via `picture/source`.
- A órbita de 48 segundos continua sendo a única animação. Movimento reduzido seleciona SVG estático.
- A foto é o arquivo original, sem alteração facial.
- A prosa usa a tipografia nativa do GitHub, porque estilos arbitrários não são confiáveis em README. Os assets mantêm a tipografia aprovada.
- Formação, experiência, stack e estudos têm texto acessível, incluindo versões recolhíveis. Imagens têm textos alternativos completos.
- Links reais para o projeto, LinkedIn, GitHub e fontes dos dados.

## Telemetria

Um painel com contagens públicas de repositórios (incluindo forks), repositórios originais (sem forks) e estrelas recebidas apenas nos originais. O horário de coleta fica visível e `telemetry.json` permite auditar os valores. Não mede produtividade, velocidade ou proficiência.

`python design/update_telemetry.py` consulta a API pública, segue paginação e gera o painel. `--from-snapshot` permite reproduzir os SVGs a partir do JSON salvo. Falhas de rede não substituem dados por zeros. A Action agenda atualização semanal e permite execução manual, com permissão de escrita somente em conteúdo. Nenhum PAT é necessário para consultar os dados públicos.

## Validação

22 SVGs foram renderizados como imagens no Chrome, com verificação dos limites dos textos. O README completo foi processado pela API de Markdown do GitHub: 10 elementos `picture`, 12 `source` e 7 `details` foram preservados.

Testes em 1440, 768, 390 e 320 px verificam carregamento de imagens, ausência de transbordamento horizontal no README, escolha de variantes móveis, abertura dos sete detalhes e seleção estática para movimento reduzido. A revisão visual inclui desktop e celular. Os PNGs e relatórios locais ficam em `design/integration/`.

## Assets anteriores sem uso no README

Permanecem no workspace como histórico, sem referências no README:

- `assets/space-hero.svg`
- `assets/hero/black-hole-accretion-disk.png`
- `assets/journey/earth-limb-airglow.jpg`
- `assets/journey/earth-limb-airglow-strip.jpg`
- `assets/footer/airglow-from-orbit.jpg`
- `assets/footer/airglow-footer-strip.jpg`
- `wp1817964-interstellar-wallpapers.jpg`

Os widgets antigos de GitHub Readme Stats e Streak Stats, e os badges Shields.io, também deixaram de ser usados.

## Dependências do titular

Nenhum screenshot é necessário para o README funcionar. Para acrescentá-los futuramente:

- Adote Já: capturas reais da tela inicial e de um fluxo central, preferencialmente 1080 × 1920 px, em `assets/projects/react-native-home.png` e `react-native-flow.png`.
- Michelc: imagem opcional, autorizada e anonimizada, preferencialmente 1600 × 900 px. A apresentação conceitual atual funciona sem ela.

Não foram inventadas capturas, métricas ou resultados.
