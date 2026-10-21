"""Etapa 5: tela Streamlit com upload, botão de processar e chat."""
import tempfile
from pathlib import Path

import streamlit as st

from busca import buscar, carregar_indice
from embeddings import PASTA_INDICE, salvar_indice
from ingestao import EXTENSOES, processar_documento, processar_pasta
from resposta import responder

st.set_page_config(page_title="RAG simples", page_icon="📄")
st.title("📄 Pergunte aos seus documentos")


def processar_arquivos(arquivos):
    # O leitor trabalha com caminhos, então gravamos o upload numa pasta
    # temporária mantendo o nome original (ele aparece na fonte do trecho).
    chunks, avisos = [], []
    with tempfile.TemporaryDirectory() as pasta:
        for arquivo in arquivos:
            # O nome vem do navegador e não é confiável: ".." ou "C:\..." nele
            # gravaria fora da pasta temporária. Path(...).name fica só com o nome.
            nome = Path(arquivo.name).name
            if Path(nome).suffix.lower() not in EXTENSOES:
                avisos.append(f"{nome}: formato não suportado.")
                continue
            caminho = Path(pasta) / nome
            caminho.write_bytes(arquivo.getvalue())
            try:
                chunks += processar_documento(caminho)
            except Exception as erro:
                # Um arquivo ruim não deve derrubar os outros.
                avisos.append(f"{nome}: não consegui ler ({erro}).")
    return chunks, avisos


def indice_existe():
    return (PASTA_INDICE / "vetores.npy").exists()


# --- Barra lateral: upload e processamento ---
with st.sidebar:
    st.header("1. Documentos")
    arquivos = st.file_uploader(
        "Envie PDF, TXT ou MD",
        type=[e.lstrip(".") for e in EXTENSOES],
        accept_multiple_files=True,
    )
    if st.button("Processar documentos"):
        with st.spinner("Lendo, cortando e gerando vetores..."):
            # Sem upload, usamos os documentos de exemplo para a demo funcionar.
            if arquivos:
                chunks, avisos = processar_arquivos(arquivos)
            else:
                chunks, avisos = processar_pasta(), []
            for aviso in avisos:
                st.warning(aviso)
            if chunks:
                salvar_indice(chunks)
                st.session_state.pop("mensagens", None)
                st.success(f"Pronto: {len(chunks)} pedaços no índice.")
            else:
                # Não salvamos nada: o índice anterior continua valendo.
                st.error("Nenhum texto foi extraído. PDFs escaneados não funcionam.")

# --- Chat ---
st.header("2. Perguntas")

if not indice_existe():
    st.info("Processe os documentos na barra lateral para começar.")
    st.stop()

# Streamlit reexecuta o script a cada interação; guardamos o histórico aqui.
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


def mostrar_trechos(trechos):
    # st.text (e não markdown): o texto vem dos documentos e não deve ser
    # interpretado como formatação, links ou imagens.
    with st.expander("Trechos usados"):
        for t in trechos:
            st.text(f"{t['arquivo']} — similaridade {t['nota']:.2f}")
            st.text(t["texto"])


for msg in st.session_state.mensagens:
    with st.chat_message(msg["papel"]):
        st.write(msg["texto"])
        if msg.get("trechos"):
            mostrar_trechos(msg["trechos"])

pergunta = st.chat_input("Faça uma pergunta sobre os documentos")
if pergunta:
    st.session_state.mensagens.append({"papel": "user", "texto": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):
        trechos = []
        try:
            with st.spinner("Buscando e respondendo..."):
                vetores, chunks = carregar_indice()
                trechos = buscar(pergunta, vetores, chunks)
                texto = responder(pergunta, trechos)
        except Exception as erro:
            # Mensagem curta no lugar do traceback completo na tela.
            texto = f"Não consegui responder: {erro}"
            st.error(texto)
        else:
            st.write(texto)
            mostrar_trechos(trechos)
    st.session_state.mensagens.append(
        {"papel": "assistant", "texto": texto, "trechos": trechos}
    )
