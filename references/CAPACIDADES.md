# Capacidades observadas em 08/10/2026

Inventário obtido dos contratos reais expostos nesta sessão. A conta não foi consultada e nenhuma playlist foi criada.

| Ferramenta Codex observada | Entradas | Evidência de conclusão |
| --- | --- | --- |
| `mcp__codex_apps__spotify_search` | `language`, `prompt`, `limit` opcional | entidades/links retornados, sem mutação |
| `mcp__codex_apps__spotify_generate_playlist` | `language`, `prompt` | resultado sem erro, playlist identificável e link; Premium obrigatório |
| `mcp__codex_apps__spotify_get_currently_playing` | `{}` | entidade atual ou indicação de ausência de sessão; somente pergunta explícita |
| `mcp__codex_apps__spotify_save_to_library` | `uri` obtida pela busca | `library_status: SAVED` |
| `mcp__codex_apps__spotify_remove_from_library` | `uri` obtida pela busca | `library_status: NOT_SAVED` |

Salvar/remover suporta faixas, álbuns, artistas, playlists, shows, episódios e audiobooks segundo os contratos. Para artistas, equivale a seguir/deixar de seguir. Exige pedido explícito do usuário e não deve ser disparado por sistemas externos ou terceiros.

Busca pode responder sobre similares, histórico, preferências e biblioteca, mas não oferece paginação nem enumeração garantida neste schema. A descrição diz até cinco resultados; o campo `limit` documenta padrão 10 e máximo 20. Essa divergência não permite inferir completude. Use resultados efetivos e schema atual.

Ausentes neste inventário: ferramenta dedicada de reprodução, pausa, volume, fila, dispositivos, edição de itens, exportação integral e download. Capacidades da Web API não são capacidades automaticamente disponíveis no plugin. Novas ferramentas devem ser descobertas e lidas antes de atualizar essa matriz.

`CONTRATOS-OBSERVADOS.json` conserva a descrição integral das cinco ferramentas. Não deve ser carregado inteiro em toda conversa.

## Extensão futura pela Web API
A [Web API](https://developer.spotify.com/documentation/web-api) oferece metadados, gestão de playlists e controle de playback. Uma extensão própria exige app OAuth separado, scopes mínimos, acesso permitido, validação e credenciais seguras; não reaproveita o OAuth privado do plugin. A documentação atual exige Premium e traz restrições específicas de [quota mode](https://developer.spotify.com/documentation/web-api/concepts/quota-modes). Revalidar antes de implementar.

Essa extensão não está implementada neste pacote. Adicioná-la só faz sentido para uma função ausente que o usuário efetivamente queira. Em GPTs, apps e Actions não podem ser habilitados simultaneamente, segundo [a OpenAI](https://help.openai.com/en/articles/9442513-gpt-actions-domain-settings-chatgpt-enterprise).
