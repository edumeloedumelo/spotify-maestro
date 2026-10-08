# Pesquisa sobre downloads — 08/10/2026

## 1. Ouvir offline no Spotify
É o caminho oficial para baixar playlists e músicas para escuta dentro do aplicativo. Premium permite álbuns, playlists e podcasts; Free permite podcasts. Para música individual, coloque-a em uma playlist e baixe a playlist. Limite documentado: 10 mil faixas por dispositivo, até cinco dispositivos; conectar pelo menos a cada 30 dias para manter os downloads. [Suporte Spotify](https://support.spotify.com/br-pt/article/listen-offline/).

No computador: abra Spotify com Internet, abra a playlist e clique em Baixar. Espere o indicador de concluído. Para testar escuta offline no Mac, use o menu Spotify → Modo offline e teste uma faixa; ao terminar, restaure o estado anterior se tiver mudado o modo para o teste. Não reinstale nem remova cache como primeira tentativa: reinstalar exige baixar novamente. [Procedimento oficial](https://support.spotify.com/br-pt/article/listen-offline/).

Automação possível no Codex: conector localiza a entidade → link retornado abre o app → controle visual disponível inspeciona e aciona o botão oficial → indicador comprova progresso/conclusão. É uma composição proposta, não testada com esta conta. Depende de controle de UI, aplicativo autenticado, plano, espaço e botão realmente acessível. O plugin sozinho não baixa; GPT com app Spotify não controla o aplicativo Mac por essa conexão.

## 2. MP3, FLAC e outros arquivos portáveis
O plugin não expõe download de áudio. A Web API não oferece uma rota para baixar gravações completas; sua documentação proíbe facilitar downloads de conteúdo Spotify ou stream ripping. Não implementar extração de cache/DRM. [Referência oficial de faixas](https://developer.spotify.com/documentation/web-api/reference/get-track).

Uma fonte que permite baixar arquivos é o Bandcamp: compras podem ser baixadas em MP3, FLAC, WAV e outros formatos. Não há garantia de que uma faixa da playlist esteja disponível nessa loja. O agente pode localizar uma edição correspondente, identificar diferenças e orientar o download da compra existente; comprar exige autorização específica. [Formatos no Bandcamp](https://get.bandcamp.help/en/articles/15263234-in-which-formats-can-i-download-my-purchases).

Arquivos que o usuário já possui podem ser organizados e usados no recurso Arquivos locais do Spotify. Isso importa a biblioteca local; não converte o catálogo do streaming em arquivos. [Arquivos locais](https://support.spotify.com/us/article/local-files/).

## 3. Exportar playlists como listas
CSV/JSON pode conter nome, artista, álbum, ID, link e posição quando esses dados estiverem disponíveis. É backup de metadados, não download de músicas. As ferramentas atuais não garantem leitura de todas as faixas; para exportação integral seria necessária outra capacidade de leitura, com paginação e acesso autorizados. Informe cobertura real e preserve o arquivo original ao revisar.

## 4. spotDL e ferramentas semelhantes
O [repositório oficial spotDL](https://github.com/spotDL/spotify-downloader) informa que procura músicas de playlists Spotify no YouTube e baixa correspondências com metadados. Portanto, o áudio vem de outra fonte e pode ser uma versão diferente. O README não comprova autorização para baixar qualquer faixa, identidade da gravação nem qualidade do original Spotify.

O projeto foi identificado e pesquisado; não foi instalado ou executado. Para um uso futuro com material cujo download seja permitido, verificar fonte, permissão, versão e dependências antes de propor execução. Não prometer “Spotify para MP3” nem fornecer credenciais/cookies a sites conversores. A preferência deste pacote é download oficial offline ou arquivo disponibilizado por fonte autorizada.

## Diagnóstico
Quando offline falhar, verificar plano, conexão, armazenamento, limite de dispositivos e estado do aplicativo. Distinguir faixa indisponível de falha geral. Não mudar assinatura, configurações de rede ou apagar downloads sem pedido. Encerrar com estado comprovado: disponível offline, em andamento, falhou ou não verificado.
