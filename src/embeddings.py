"""Etapa 2: embeddings e construção do índice (só arquivos, sem banco)."""
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from ingestao import processar_pasta

NOME_MODELO = "paraphrase-multilingual-MiniLM-L12-v2"
PASTA_INDICE = Path(__file__).resolve().parent.parent / "indice"

_modelo = None


def carregar_modelo():
    # Carrega uma vez só: abrir o modelo é lento e a pergunta usa o mesmo.
    global _modelo
    if _modelo is None:
        _modelo = SentenceTransformer(NOME_MODELO)
    return _modelo


def gerar_vetores(textos):
    # Normalizar deixa o cosseno virar um simples produto escalar na busca.
    return carregar_modelo().encode(textos, normalize_embeddings=True)


def salvar_indice(chunks, pasta=PASTA_INDICE):
    # Sem texto extraído (ex.: PDF escaneado) não há o que indexar; salvar
    # um índice vazio só quebraria a busca depois, longe da causa.
    if not chunks:
        raise ValueError("Nenhum texto foi extraído dos documentos.")
    pasta.mkdir(exist_ok=True)
    vetores = gerar_vetores([c["texto"] for c in chunks])
    np.save(pasta / "vetores.npy", vetores)
    (pasta / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return vetores


if __name__ == "__main__":
    chunks = processar_pasta()
    vetores = salvar_indice(chunks)
    print(f"{len(chunks)} pedaços em chunks.json")
    print(f"vetores.npy com formato {vetores.shape}")
