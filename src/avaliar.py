"""Etapa 6: roda as perguntas do eval e conta os acertos."""
import json
from pathlib import Path

from busca import buscar
from embeddings import gerar_vetores
from ingestao import processar_pasta
from resposta import responder

ARQUIVO_PERGUNTAS = Path(__file__).resolve().parent.parent / "eval" / "perguntas.json"


def disse_que_nao_encontrou(resposta):
    # O modelo pode escrever "não encontrei" ou "não encontrado"; o começo basta.
    return "não encontr" in resposta.lower()


def avaliar_pergunta(item, vetores, chunks):
    pergunta = item["pergunta"]
    esperado = item["documento_esperado"]
    trechos = buscar(pergunta, vetores, chunks)

    if esperado is None:
        # Fora da base: o que importa é o modelo admitir que não sabe.
        # Só chamamos o modelo aqui, para o eval dos outros casos ser rápido e grátis.
        acertou = disse_que_nao_encontrou(responder(pergunta, trechos))
    else:
        acertou = esperado in {t["arquivo"] for t in trechos}

    recuperados = ", ".join(sorted({t["arquivo"] for t in trechos}))
    return {"pergunta": pergunta, "esperado": esperado, "recuperados": recuperados, "acertou": acertou}


def main():
    perguntas = json.loads(ARQUIVO_PERGUNTAS.read_text(encoding="utf-8"))
    # O índice é montado em memória a partir de data/amostras/. Ler o de indice/
    # misturaria o eval com o que o usuário enviou pelo app (as perguntas
    # falam dos documentos de exemplo) e deixa o índice em disco intacto.
    chunks = processar_pasta()
    vetores = gerar_vetores([c["texto"] for c in chunks])

    resultados = [avaliar_pergunta(p, vetores, chunks) for p in perguntas]

    print(f"{'OK':<4}{'Pergunta':<55}Esperado")
    print("-" * 100)
    for r in resultados:
        marca = "SIM" if r["acertou"] else "NÃO"
        print(f"{marca:<4}{r['pergunta']:<55}{r['esperado'] or '(não está na base)'}")
        if not r["acertou"]:
            print(f"    recuperou: {r['recuperados']}")

    acertos = sum(r["acertou"] for r in resultados)
    print(f"\nTotal: {acertos}/{len(resultados)}")


if __name__ == "__main__":
    main()
