# Configuração pronta — GPT Spotify Maestro

## Campos
**Nome:** Spotify Maestro

**Descrição:** Assistente pessoal para descobrir músicas, criar playlists privadas, organizar a biblioteca Spotify e orientar downloads oficiais offline, conforme as ferramentas conectadas.

**Instruções:** cole todo o arquivo `INSTRUCOES.md` no campo de instruções. Ele é autocontido.

**Iniciadores de conversa:**
- Busque playlists de jazz instrumental para estudar.
- Crie uma playlist de rock brasileiro para uma viagem de 90 minutos.
- O que está tocando agora no Spotify?
- Como baixar uma playlist para ouvir offline no meu Mac?

**Conhecimento opcional:** envie `references/CAPACIDADES.md` e `references/DOWNLOADS.md`. Não envie tokens, credenciais nem histórico pessoal. Os contratos integrais ficam como evidência local, sem necessidade de upload.

**Capacidades:** habilite apps e conecte Spotify, se essa opção existir na conta/workspace. Busca web ajuda a revalidar suporte e documentação. Análise de dados é opcional para CSV/JSON com dados fornecidos. Não precisa de imagem ou Canvas. Não fixe modelo ausente do seletor.

**Actions:** não adicionar nesta configuração baseada em apps; a OpenAI informa que GPTs usam apps ou Actions, sem combinação simultânea. Não há schema de Action neste pacote, pois ele usará a conexão oficial existente.

## Aplicação
No ChatGPT web, acesse GPTs → Criar se sua conta/workspace for elegível, ou edite um GPT existente. Preencha os campos acima, conecte Spotify, teste no Preview e salve com visibilidade privada. Compartilhar/publicar exige pedido específico.

As ferramentas podem ter nomes diferentes dos nomes internos Codex. Confira funções e schemas disponíveis no próprio GPT. Upload de arquivo ou nome “Spotify” no prompt não cria conexão. Se apps/Spotify não estiverem disponíveis no editor, informe a limitação; não adicione Actions ou outro serviço silenciosamente.

Alternativa imediata: use `INSTRUCOES.md` como mensagem inicial de um chat normal no ChatGPT com app Spotify conectado. Esse uso não cria GPT registrado nem garante que o chat tenha todas as cinco ferramentas observadas no Codex. Também pode servir como texto de instruções reutilizáveis numa superfície de plugins que a conta oferecer; publicação/instalação devem seguir o fluxo real dessa superfície.

## Disponibilidade verificada em 08/10/2026
A [OpenAI](https://help.openai.com/en/articles/8554407-gpts-in-chatgpt) informa que contas pessoais não podem criar novos GPTs; GPTs existentes continuam utilizáveis e sua edição depende de elegibilidade. Em workspaces gerenciados, criação/edição dependem de permissões. A página também anuncia aposentadoria planejada de GPTs e migração para plugins; confira avisos da conta antes de investir em publicação.

O [guia de edição](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts) descreve apps e Actions como opções mutuamente exclusivas. O pacote entrega as instruções e configuração, mas não salva o GPT na conta automaticamente.
