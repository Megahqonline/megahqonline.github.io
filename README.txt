MEGAHQ ONLINE — PACOTE PROFISSIONAL

ARQUIVOS
- index.html: página inicial nova.
- leitor.html: cópia byte a byte do leitor original enviado; preserva a lógica e os scripts que existiam no arquivo original.
- artigos e páginas institucionais: páginas editoriais e informativas.
- assets/: estilos e script compartilhados das páginas internas.

PUBLICAÇÃO NO GITHUB PAGES
1. Extraia todos os arquivos e pastas.
2. Envie todos os arquivos para a raiz do repositório Megahqonline/megahqonline.github.io.
3. Substitua o index.html antigo pelo novo index.html.
4. Adicione leitor.html e assets/ mantendo exatamente os nomes e a estrutura.
5. Não apague as páginas de artigos e institucionais.
6. Faça Commit changes e aguarde a publicação.

COMPORTAMENTO DOS LINKS
- https://megahqonline.github.io/ abre a página inicial.
- https://megahqonline.github.io/leitor.html abre o leitor diretamente.
- Links antigos do formato /?id=... ou /?pdf=... são encaminhados diretamente para leitor.html preservando a query string; não há página intermediária de confirmação.

OBSERVAÇÕES
- O leitor foi copiado sem alterar seu código, mas deve ser testado em produção após publicação.
- Os metadados AdMaven e Monetag foram mantidos na página inicial e no leitor, conforme os arquivos recebidos. Isso não garante aprovação ou funcionamento de serviços de terceiros.
- Preencha o e-mail de contato em contato.html antes de publicar.
- A página inicial usa fontes Google Fonts com fallback local; o layout continua legível se elas não carregarem.
