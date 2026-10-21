"""Etapa 3: busca por similaridade no índice."""
import json

import numpy as np

from embeddings import PASTA_INDICE, gerar_vetores

TOP_K = 3


def carregar_indice(pasta=PASTA_INDICE):
    arquivo_vetores = pasta / "vetores.npy"
    arquivo_chunks = pasta / "chunks.json"
    if not (arquivo_vetores.exists() and arquivo_chunks.exists()):
        raise FileNotFoundError("Índice não encontrado. Processe os documentos primeiro.")
    # allow_pickle=False: o .npy só pode conter números, nunca código.
    vetores = np.load(arquivo_vetores, allow_pickle=False)
    chunks = json.loads(arquivo_chunks.read_text(encoding="utf-8"))
    # Um arquivo de cada época daria trechos trocados, sem nenhum erro visível.
    if len(vetores) != len(chunks):
        raise ValueError("Índice inconsistente: reprocesse os documentos.")
    return vetores, chunks


def buscar(pergunta, vetores, chunks, top_k=TOP_K):
    # Os vetores já são normalizados, então produto escalar = cosseno.
    vetor_pergunta = gerar_vetores([pergunta])[0]
    notas = vetores @ vetor_pergunta
    melhores = np.argsort(notas)[::-1][:top_k]
    return [{**chunks[i], "nota": float(notas[i])} for i in melhores]


if __name__ == "__main__":
    vetores, chunks = carregar_indice()
    pergunta = "Qual o prazo do reembolso?"
    print(f"Pergunta: {pergunta}\n")
    for r in buscar(pergunta, vetores, chunks):
        print(f"[{r['arquivo']}] nota {r['nota']:.2f}")
        print(r["texto"][:300].replace("\n", " "), "...\n")
