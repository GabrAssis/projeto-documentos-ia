# Assistente de Documentos com IA

**Consulta a documentos em português com busca semântica e exibição das fontes recuperadas.**

Aplicação educacional de RAG que conecta documentos PDF, TXT e Markdown a uma interface de perguntas e respostas. Combina processamento de texto, embeddings locais e geração de respostas com um modelo de linguagem.

[Código](src/) · [Exemplos](data/amostras/) · [Avaliação](eval/perguntas.json) · [Guia de execução](docs/execucao.md)

## Problema de negócio

Como facilitar a consulta a políticas e procedimentos sem procurar manualmente cada informação em arquivos diferentes?

A demonstração utiliza documentos fictícios sobre trabalho híbrido, segurança da informação e reembolso de despesas.

## Entregas

- Leitura de documentos PDF, TXT e Markdown.
- Divisão dos textos em trechos com sobreposição.
- Geração local de embeddings multilíngues.
- Busca por similaridade de cosseno.
- Geração de respostas com os trechos recuperados como contexto.
- Exibição dos arquivos de origem e das notas de similaridade.
- Interface Streamlit para upload, processamento e perguntas.
- Rotina de avaliação e comparação de tamanhos de trecho.

## Decisões técnicas

| Decisão | Aplicação |
| --- | --- |
| Embeddings locais | Representação vetorial dos textos no próprio ambiente. |
| Índice em arquivos | Vetores em NumPy e trechos em JSON. |
| Módulos separados | Ingestão, embeddings, busca, resposta e interface. |
| Contexto documental | Instrução para responder a partir dos trechos fornecidos. |
| Avaliação própria | Perguntas com documento esperado e um caso fora da base. |

## Tecnologias

Python · Streamlit · pypdf · Sentence Transformers · NumPy · Anthropic · python-dotenv

## Executar

Siga o [guia de execução](docs/execucao.md) para preparar o ambiente e configurar a chave de API. Depois:

```powershell
python -m streamlit run src/app.py
```

A demonstração é de uso local e inclui três PDFs fictícios.

## Contexto

Projeto desenvolvido passo a passo em aula de Engenharia de Dados com IA e publicado no portfólio de Gabriel de Assis.
