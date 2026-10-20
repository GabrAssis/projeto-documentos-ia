# Assistente de Documentos com IA

**Consulta a documentos em português com busca semântica e exibição das fontes recuperadas.**

Projeto educacional de RAG que combina processamento de documentos, embeddings locais e geração de respostas com um modelo de linguagem.

## Problema de negócio

Como facilitar a consulta a políticas e procedimentos sem procurar manualmente cada informação em arquivos diferentes?

A demonstração utiliza documentos fictícios sobre trabalho híbrido, segurança da informação e reembolso de despesas.

## Entregas

- Leitura de documentos PDF, TXT e Markdown.
- Divisão dos textos em trechos com sobreposição.
- Geração local de embeddings multilíngues.
- Recuperação de trechos por similaridade de cosseno.
- Geração de respostas com os trechos recuperados como contexto.
- Exibição dos arquivos de origem e das notas de similaridade.
- Interface Streamlit para upload, processamento e perguntas.
- Rotina de avaliação com perguntas de referência.

## Explorar a implementação

O código, os documentos de exemplo e as instruções de execução são mantidos no repositório de estudos de Engenharia de Dados:

**[Acessar código e documentação](https://github.com/GabrAssis/Pos-Engenharia-Dados/tree/main/Engenharia-de-Dados-IA/Projeto-Documentos-IA)**

## Exemplos de uso

- Qual é o prazo para solicitar reembolso?
- Quantos caracteres uma senha precisa ter?
- Quais são os dias presenciais obrigatórios?
- Qual é o valor do auxílio home office?

## Decisões técnicas

| Decisão | Aplicação |
| --- | --- |
| Embeddings locais | Representação vetorial dos textos no próprio ambiente. |
| Índice em arquivos | Armazenamento dos vetores em NumPy e dos trechos em JSON. |
| Módulos separados | Organização entre ingestão, embeddings, busca, resposta e interface. |
| Contexto documental | Instrução para responder a partir dos trechos fornecidos. |
| Avaliação própria | Perguntas com documento esperado e um caso fora da base. |

## Tecnologias

Python · Streamlit · Sentence Transformers · NumPy · pypdf · Anthropic

## Contexto

Projeto desenvolvido em aula de Engenharia de Dados com IA e publicado no portfólio de Gabriel de Assis. Os documentos de exemplo são fictícios.
