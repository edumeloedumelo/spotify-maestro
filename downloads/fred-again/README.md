# Lote Fred again

Lista de 50 faixas consultada em 04/11/2026 na [playlist Spotify](https://open.spotify.com/playlist/37i9dQZF1DZ06evO2zE29q). O manifesto é uma fotografia dessa data; executar o script não atualiza a playlist.

`download.py` procura correspondências no YouTube, verifica título, artista, versão e duração, converte para MP3 VBR, grava tags ID3 e testa a decodificação integral com FFmpeg. Qualidade e identidade não são garantidas apenas pela semelhança do título e duração. Use com material cujo download seja permitido.

As fontes revisadas estão em `reviewed-sources.json`. Uma exceção explícita é **Piensas En Mi**: o catálogo oficial da Atlantic Records UK no YouTube fornece aproximadamente 3min02s para os mesmos artistas e álbum; o Spotify informa 3min18s. Essa diferença é preservada no relatório, sem estender nem cortar o áudio.

## Executar

Depois de instalar as dependências indicadas no README principal, execute na raiz do repositório:

```bash
source .venv/bin/activate
python downloads/fred-again/download.py
python downloads/fred-again/deliver.py --check-only
python downloads/fred-again/deliver.py
```

O último comando copia o lote completo para `~/Music/fred again`. Para outro destino:

```bash
python downloads/fred-again/deliver.py --output "$HOME/Music/minha playlist"
```

O script preserva destinos diferentes e interrompe a cópia em caso de conflito. O relatório contém as fontes, hashes e diferenças de duração. A playlist M3U8 mantém a ordem original. Não apague `relatorio.json` se quiser retomar e preservar a rastreabilidade.

Para retomar, execute novamente o download. Arquivos já registrados e com hash íntegro são reaproveitados. Para tentar somente posições específicas:

```bash
python downloads/fred-again/download.py 4 13 18 --workers 2
```

Falhas de rede, indisponibilidade ou ausência de correspondência ficam pendentes no relatório. `deliver.py` exige o lote completo validado. Não altere a duração esperada apenas para fazer uma faixa passar: confira a fonte e documente uma exceção revisada quando aplicável.

## Evidência desta entrega

O lote original teve 50 arquivos MP3 decodificados integralmente, títulos conferidos e cópia verificada por SHA-256: 370.049.321 bytes. Houve uma exceção de duração, descrita acima. Os MP3 e relatórios de execução locais não fazem parte do repositório.

Para a versão compartilhável, os caminhos foram ajustados para o usuário atual e as dependências são localizadas pelo PATH. A validação de entrega foi executada sobre os 50 arquivos existentes; um novo download completo em outro computador ainda depende de execução nesse ambiente.
