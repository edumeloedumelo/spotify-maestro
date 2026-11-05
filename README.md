# Spotify Maestro

Agente para usar o Spotify no Codex, com instruções para ChatGPT e scripts opcionais de organização e download de áudio de fontes externas. Cada pessoa conecta sua própria conta; o repositório não contém credenciais nem arquivos de música.

## Começar em outro Mac

1. Tenha acesso a este repositório no GitHub. Se ele estiver privado, o proprietário precisa conceder acesso antes do clone.
2. Clone pelo Terminal e abra a pasta no Codex:

```bash
git clone https://github.com/edumeloedumelo/spotify-maestro.git
cd spotify-maestro
```

3. Habilite o plugin Spotify no Codex e conecte sua própria conta pela interface.
4. Abra um chat neste projeto e cole o texto de [INICIO-CODEX.md](INICIO-CODEX.md).

As instruções do agente funcionam sem instalar Python. Para os scripts opcionais de áudio, com Homebrew já instalado:

```bash
brew install python ffmpeg deno
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-downloads.txt
```

## Atualização de 04/11/2026

Adicionado o [fluxo Fred again](downloads/fred-again/README.md): manifesto de 50 faixas, fontes revisadas, download retomável, metadados ID3, decodificação completa e cópia conferida por SHA-256 para a pasta Música do usuário atual. Os scripts usam FFmpeg e Deno encontrados no PATH, sem caminhos pessoais fixos.

```bash
source .venv/bin/activate
python downloads/fred-again/download.py
python downloads/fred-again/deliver.py --check-only
python downloads/fred-again/deliver.py
```

A entrega original teve 50 MP3 validados. Uma faixa, **Piensas En Mi**, possui diferença de duração entre a fonte oficial encontrada e o Spotify; ela está documentada. O GitHub contém código e listas, não os MP3. Esses scripts buscam correspondências no YouTube e não extraem áudio do Spotify. Utilize fontes cujo download seja permitido.

O manifesto é fixo: para outra playlist, peça ao agente que consulte todos os itens disponíveis pelo conector e prepare um novo lote. As capacidades dependem das ferramentas efetivamente conectadas na sessão.

## Histórico — 08/10/2026

A playlist privada `nova 1` foi criada e conferida com as 60 músicas curtidas mais recentes: https://open.spotify.com/playlist/124g8PR21PRg3UpDaYbxxr.

O spotDL encontrou limite de consultas na API do Spotify, com espera indicada de 86400 segundos. A alternativa em `downloads/` usa nomes, artistas e duração já observados, sem consultar a API do Spotify, e baixa correspondências do YouTube. Foram salvos e verificados 57 MP3. Três versões ficaram pendentes: David Fritz — Flying Saucer; So Good — meera Remix; Marshall Jefferson — Move Your Body (6min45s). Similaridade e duração não garantem identidade das gravações.

Os MP3 originais estão em `~/Music/nova 1`. O repositório guarda instruções, scripts e a lista de faixas; áudio e credenciais são ignorados pelo Git. O backup das músicas fica no iCloud Drive em `Music Edu/nova 1`.

### Executar os scripts de download no Mac

Requer Python com `yt-dlp` e `rapidfuzz`, FFmpeg em `/opt/homebrew/bin` e Deno em `~/.spotdl/deno`. Na máquina usada nesta entrega, essas dependências estão instaladas no ambiente `~/spotdl-env`.

```bash
source "$HOME/spotdl-env/bin/activate"
python downloads/baixar_nova_1.py
```

Execute dentro da pasta deste repositório. O script preserva os MP3 já existentes, registra fontes e pendências em `~/Music/nova 1/relatorio-download.json` e tenta duas faixas por vez. Use `--retry-failed` somente após corrigir a causa da falha. O script `revisar_pendencias.py` registra a recuperação específica realizada nesta entrega.

## Estrutura original
```text
spotify-maestro/
├── AGENTS.md
├── README.md
├── INICIO-CODEX.md
├── gpt/
│   ├── CONFIGURACAO.md
│   └── INSTRUCOES.md
├── references/
│   ├── CAPACIDADES.md
│   ├── CONTRATOS-OBSERVADOS.json
│   └── DOWNLOADS.md
└── evals/
    └── ACEITACAO.md
```

## Uso do agente
1. Adicione como projeto local a pasta em que você clonou este repositório.
2. Habilite o plugin Spotify no Codex e conecte sua conta pela interface se solicitado. Não precisa de chave OpenAI nem Spotify Developer para este caminho.
3. Abra um chat nesse projeto e cole `INICIO-CODEX.md`. O `AGENTS.md` define o agente em cada chat do projeto. Não é um processo autônomo em segundo plano.
4. Comece com “Busque playlists de jazz instrumental para estudar”. Confira uma resposta real com link. Só depois solicite mudanças desejadas.
5. Para offline, peça “Baixe esta playlist para ouvir offline no Spotify deste Mac”. O agente tentará a UI somente se disponível; caso contrário, orientará o botão oficial. Nenhum download está ativo agora.

Para levar o projeto a outra pasta, copie a pasta inteira preservando a estrutura. Não substitua o `AGENTS.md` de um projeto diferente: faça a instalação em uma pasta própria. As instruções do agente não exigem Python/Node. Os scripts opcionais de download exigem as dependências indicadas acima; as funções do Spotify dependem do plano e das capacidades disponíveis na sua conta.

## GPT / ChatGPT — configuração e registro histórico
Leia `gpt/CONFIGURACAO.md`. O conteúdo de `gpt/INSTRUCOES.md` é completo e pode ser colado como instruções; referências são material de apoio. Conectar Spotify no Codex não conecta automaticamente o ChatGPT.

Em 08/10/2026, a [documentação OpenAI](https://help.openai.com/en/articles/8554407-gpts-in-chatgpt) informa que novas criações de GPT estão indisponíveis em contas pessoais; workspaces Business, Enterprise e Edu dependem de permissões. Também anuncia migração para plugins. Se seu editor não oferecer criação/apps, use o mesmo texto em um chat do ChatGPT com Spotify conectado, ou edite um GPT existente elegível. Esse caminho preserva instruções, mas só o inventário real confirma quais operações podem executar.

## Entradas, saídas e conclusão
Entrada: pedido em linguagem natural, critérios musicais, entidade/link quando necessário e conta conectada pela plataforma. Saída: entidades com links, playlist privada criada, resultado de biblioteca ou procedimento offline verificado/limitado.

Concluído: instruções instaladas na superfície escolhida, ferramentas descobertas e operação de leitura validada. Funcionalidades de escrita/offline são aceitas somente após testes autorizados com resultado real. `evals/ACEITACAO.md` distingue revisão documental de testes ainda pendentes.

Para desfazer a instalação local, remova esse projeto do Codex; preserve os arquivos se quiser reutilizar. Desconectar o app pela plataforma encerra o acesso do conector. Essas ações não desfazem playlists criadas ou mudanças de biblioteca, que precisam ser revertidas especificamente.

