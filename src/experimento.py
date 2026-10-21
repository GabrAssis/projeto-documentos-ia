"""Etapa 7: compara tamanhos de chunk rodando o mesmo eval em cada um."""
import json

from avaliar import ARQUIVO_PERGUNTAS, avaliar_pergunta
from embeddings import gerar_vetores
from ingestao import SOBREPOSICAO, TAMANHO_CHUNK, processar_pasta

# 800 entra como referência para comparar com os outros dois.
TAMANHOS = [400, TAMANHO_CHUNK, 1500]


def rodar_com_tamanho(tamanho, perguntas):
    # Tudo em memória: não mexe em indice/, então não apaga o índice que
    # o app está usando (por exemplo, o de documentos enviados pelo usuário).
    chunks = processar_pasta(tamanho=tamanho, sobreposicao=SOBREPOSICAO)
    vetores = gerar_vetores([c["texto"] for c in chunks])
    resultados = [avaliar_pergunta(p, vetores, chunks) for p in perguntas]
    return len(chunks), resultados


def main():
    perguntas = json.loads(ARQUIVO_PERGUNTAS.read_text(encoding="utf-8"))
    resumo = []
    for tamanho in TAMANHOS:
        total_chunks, resultados = rodar_com_tamanho(tamanho, perguntas)
        acertos = sum(r["acertou"] for r in resultados)
        erradas = [r["pergunta"] for r in resultados if not r["acertou"]]
        resumo.append((tamanho, total_chunks, acertos, erradas))

    print(f"\n{'Chunk':<8}{'Pedaços':<10}{'Acertos'}")
    print("-" * 30)
    for tamanho, total_chunks, acertos, erradas in resumo:
        print(f"{tamanho:<8}{total_chunks:<10}{acertos}/{len(perguntas)}")
        for pergunta in erradas:
            print(f"    errou: {pergunta}")


if __name__ == "__main__":
    main()
