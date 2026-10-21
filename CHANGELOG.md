# CHANGELOG

- Etapa 0: criado .venv, requirements.txt, .gitignore e .env.example; bibliotecas instaladas.
- Etapa 1: criado src/ingestao.py (lê PDF/txt/md e corta em chunks de 800 com 100 de sobreposição); amostras copiadas para data/amostras/.
- Etapa 2: criado src/embeddings.py; gera vetores (384 números) com paraphrase-multilingual-MiniLM-L12-v2 e salva indice/vetores.npy e indice/chunks.json (9 pedaços).
- Etapa 3: criado src/busca.py; carrega o índice e devolve os 3 trechos mais parecidos (cosseno) para uma pergunta.
- Etapa 4: criado src/resposta.py; envia pergunta + 3 trechos ao modelo de chat e responde só com base neles (diz "não encontrei" para perguntas fora da base).
- Etapa 5: criado src/app.py (Streamlit); upload de PDF/txt/md, botão de processar e chat que mostra a resposta e os 3 trechos com arquivo e similaridade.
- Etapa 6: criados eval/perguntas.json (5 perguntas) e src/avaliar.py; mostra a tabela e o total. Resultado com chunks de 800: 5/5.
- Correção (Etapa 5): criado .streamlit/config.toml desligando o observador de arquivos, que despejava tracebacks de `torchvision` no terminal ao abrir o app.
- Etapa 7: criado src/experimento.py; resultado do eval por tamanho de chunk (sobreposição 100): 400 → 21 pedaços, 5/5; 800 → 9 pedaços, 5/5; 1500 → 6 pedaços, 5/5. Sem diferença: as 5 perguntas são fáceis para uma base de 3 documentos. Índice restaurado para 800.
- Revisão de segurança e bugs: corrigidos app exposto na rede, injeção de prompt/imagem markdown, nome de upload, eval e experimento dependentes do índice em disco, MODELO_CHAT vazio, índice vazio/inconsistente, leitura de txt não UTF-8; dependências fixadas.
