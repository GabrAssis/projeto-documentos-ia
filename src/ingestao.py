"""Etapa 1: leitura dos documentos e chunking."""
from pathlib import Path

from pypdf import PdfReader

TAMANHO_CHUNK = 800
SOBREPOSICAO = 100
EXTENSOES = {".pdf", ".txt", ".md"}
PASTA_AMOSTRAS = Path(__file__).resolve().parent.parent / "data" / "amostras"


def ler_pdf(caminho):
    leitor = PdfReader(caminho)
    # PDF com senha não entrega texto; melhor avisar do que indexar vazio.
    if leitor.is_encrypted:
        raise ValueError(f"{Path(caminho).name}: PDF protegido por senha.")
    return "\n".join(pagina.extract_text() or "" for pagina in leitor.pages)


def ler_documento(caminho):
    caminho = Path(caminho)
    if caminho.suffix.lower() == ".pdf":
        return ler_pdf(caminho)
    # "replace" troca bytes inválidos por "�" em vez de derrubar o programa
    # com arquivos salvos em outra codificação (ex.: latin-1 do Bloco de Notas).
    return caminho.read_text(encoding="utf-8-sig", errors="replace")


def cortar_em_chunks(texto, tamanho=TAMANHO_CHUNK, sobreposicao=SOBREPOSICAO):
    # A sobreposição evita partir uma ideia no meio: o fim de um pedaço
    # reaparece no começo do próximo.
    passo = tamanho - sobreposicao
    # Passo <= 0 faria o range() falhar (ou nunca avançar); melhor barrar aqui.
    if passo <= 0:
        raise ValueError("A sobreposição precisa ser menor que o tamanho do chunk.")
    chunks = []
    for inicio in range(0, len(texto), passo):
        pedaco = texto[inicio:inicio + tamanho].strip()
        if pedaco:
            chunks.append(pedaco)
        if inicio + tamanho >= len(texto):
            break
    return chunks


def processar_documento(caminho, tamanho=TAMANHO_CHUNK, sobreposicao=SOBREPOSICAO):
    # Guardamos o nome do arquivo para mostrar a fonte e para a avaliação.
    texto = ler_documento(caminho)
    return [
        {"arquivo": Path(caminho).name, "texto": pedaco}
        for pedaco in cortar_em_chunks(texto, tamanho, sobreposicao)
    ]


def processar_pasta(pasta=PASTA_AMOSTRAS, tamanho=TAMANHO_CHUNK, sobreposicao=SOBREPOSICAO):
    chunks = []
    for caminho in sorted(Path(pasta).iterdir()):
        if caminho.suffix.lower() in EXTENSOES:
            chunks += processar_documento(caminho, tamanho, sobreposicao)
    return chunks


if __name__ == "__main__":
    todos = processar_pasta()
    contagem = {}
    for chunk in todos:
        contagem[chunk["arquivo"]] = contagem.get(chunk["arquivo"], 0) + 1
    for arquivo, quantidade in contagem.items():
        print(f"{arquivo}: {quantidade} pedaços")
    print(f"\nTotal: {len(todos)} pedaços. Exemplo:\n")
    print(f"[{todos[0]['arquivo']}]\n{todos[0]['texto']}")
