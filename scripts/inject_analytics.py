#!/usr/bin/env python3
"""Adiciona o Google Analytics 4 aos artigos artigo-*.html sem duplicar o código."""
from pathlib import Path

MEASUREMENT_ID = "G-0VKHN7FFB9"
TAG = f'''<!-- Google Analytics 4 - MegaHQ Online -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{MEASUREMENT_ID}');
</script>'''

ROOT = Path(__file__).resolve().parent.parent
files = sorted(ROOT.glob("artigo-*.html"))
changed = 0
for path in files:
    html = path.read_text(encoding="utf-8")
    if MEASUREMENT_ID in html:
        print(f"Já contém Analytics: {path.name}")
        continue
    if "</head>" not in html.lower():
        print(f"AVISO: não encontrei </head>; arquivo ignorado: {path.name}")
        continue
    # Substitui apenas a primeira ocorrência, preservando o restante do HTML.
    lower = html.lower()
    pos = lower.find("</head>")
    html = html[:pos] + TAG + "\n" + html[pos:]
    path.write_text(html, encoding="utf-8")
    changed += 1
    print(f"Analytics adicionado: {path.name}")
print(f"Concluído: {changed} arquivo(s) atualizado(s) de {len(files)} artigo(s).")
