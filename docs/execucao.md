# RAG simples, sem banco de dados

Um sistema de perguntas e respostas sobre documentos (PDF, TXT e MD), construído
passo a passo em uma aula ao vivo. A ideia é que dê para **ler o código inteiro e
entender cada peça**: funções pequenas, nomes em português, sem banco de dados.

**RAG** (*Retrieval-Augmented Generation*) = primeiro **buscamos** os trechos dos
documentos que têm a ver com a pergunta, depois pedimos a um modelo de linguagem
que **responda usando só esses trechos**.

```
PDF/TXT/MD → chunks → embeddings → índice (arquivos)
                                         │
pergunta → embedding → similaridade → top-3 trechos → Claude → resposta + fontes
```

## O que ele faz

- Lê `.pdf`, `.txt` e `.md`.
- Corta o texto em pedaços de 800 caracteres, com 100 de sobreposição.
- Gera embeddings **no seu computador** (modelo `paraphrase-multilingual-MiniLM-L12-v2`,
  entende português, vetores de 384 números).
- Guarda o índice em dois arquivos: `indice/vetores.npy` e `indice/chunks.json`.
- Responde com a API da Anthropic usando os 3 trechos mais parecidos
  e diz "não encontrei" quando a resposta não está nos documentos.
- Mostra os trechos usados, com o arquivo de origem e a nota de similaridade.
- Tem um eval com perguntas de teste para medir se o sistema acerta.

## Requisitos

- Python 3.11 ou superior
- Uma chave da API da Anthropic
- Internet na primeira execução (o modelo de embedding, ~120 MB, é baixado uma vez)

## Instalação

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac / Linux

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Configurar a chave
copy .env.example .env          # Windows
cp .env.example .env            # Mac / Linux
```

Abra o `.env` e preencha:

```
ANTHROPIC_API_KEY=sua-chave-aqui
MODELO_CHAT=claude-haiku-4-5-20251001
```

> O `.env` está no `.gitignore`. **Nunca** suba a chave para o GitHub.

## Como usar

### Pela tela (Streamlit)

```bash
streamlit run src/app.py
```

Abra http://localhost:8501, envie os arquivos na barra lateral e clique em
**Processar documentos**. Sem upload, o botão usa os documentos de exemplo de
`data/amostras/`. Depois é só perguntar no chat.

### Pelo terminal

Cada módulo pode ser executado sozinho, na ordem do pipeline:

```bash
python src/ingestao.py     # lê e corta os documentos de exemplo
python src/embeddings.py   # gera os vetores e salva o índice
python src/busca.py        # mostra os 3 trechos mais parecidos
python src/resposta.py     # pergunta + trechos → resposta do modelo
python src/avaliar.py      # roda o eval e mostra o total de acertos
python src/experimento.py  # compara tamanhos de chunk (400, 800, 1500)
```

## Estrutura do projeto

```
.
├── src/
│   ├── ingestao.py     leitura e chunking
│   ├── embeddings.py   gera os vetores e salva o índice
│   ├── busca.py        carrega o índice e calcula a similaridade
│   ├── resposta.py     monta o prompt e chama o modelo de chat
│   ├── app.py          tela Streamlit
│   ├── avaliar.py      roda o eval
│   └── experimento.py  compara tamanhos de chunk
├── data/amostras/      documentos de exemplo (3 PDFs)
├── eval/perguntas.json perguntas de teste
├── indice/             gerado: vetores.npy e chunks.json (fora do git)
├── .streamlit/         configuração do Streamlit
└── CHANGELOG.md        o que mudou em cada etapa
```

## Como funciona

**Caminho de um documento**

1. **Leitura**: extrai o texto puro (`pypdf` para PDF).
2. **Chunking**: pedaços de 800 caracteres com 100 de sobreposição, para não partir
   uma ideia no meio. Cada pedaço guarda o nome do arquivo.
3. **Embedding**: cada pedaço vira um vetor normalizado.
4. **Índice**: vetores em `vetores.npy`, textos em `chunks.json`. Sem banco, só arquivo.

**Caminho de uma pergunta**

1. A pergunta vira vetor com o mesmo modelo.
2. Similaridade de cosseno contra todos os vetores (como estão normalizados,
   basta um produto escalar).
3. Pega os 3 pedaços mais parecidos (top-k = 3).
4. Envia pergunta + trechos ao modelo com a instrução: *"Responda só com base nos
   trechos. Se a resposta não estiver neles, diga que não encontrou."*
5. Mostra a resposta e, abaixo, os trechos com arquivo e nota.

## Avaliação

`eval/perguntas.json` guarda perguntas e o documento esperado:

```json
{ "pergunta": "Qual o valor do auxílio home office?",
  "documento_esperado": "politica-trabalho-hibrido.pdf" }
```

- O eval e o experimento montam o índice em memória a partir de `data/amostras/`;
  não usam nem alteram o `indice/` do app.
- **Acerto** = o documento esperado aparece entre os 3 trechos recuperados.
- Pergunta com `documento_esperado: null` acerta se a resposta disser que não encontrou.

### Experimento: tamanho do chunk

| Chunk | Pedaços | Acertos |
|---|---|---|
| 400 | 21 | 5/5 |
| 800 | 9 | 5/5 |
| 1500 | 6 | 5/5 |

Os três empataram: com 3 documentos e 5 perguntas diretas, o eval é fácil demais
para separar as configurações. Para ver diferença de verdade, o próximo passo é
adicionar perguntas mais difíceis (detalhes de tabelas, anexos de dúvidas frequentes).

## Decisões de projeto

- **Sem banco de dados**: com poucos documentos, um arquivo `.npy` e um `.json`
  bastam e deixam tudo visível.
- **Embeddings locais**: não gastam API e funcionam offline depois do download.
- **Só 6 bibliotecas**: `streamlit`, `pypdf`, `sentence-transformers`, `numpy`,
  `anthropic` e `python-dotenv`.

## Limitações

- Uso local: o app escuta só em `127.0.0.1` e o índice é um só, compartilhado
  entre sessões. Não é feito para ser publicado na internet (sem autenticação).
- Os trechos enviados ao modelo são tratados como dados, mas injeção de prompt
  não tem solução definitiva: não envie documentos de origem desconhecida.
- O índice é refeito do zero a cada processamento (não é incremental).
- A busca compara a pergunta com todos os vetores; serve para centenas de
  documentos, não para milhões.
- PDFs escaneados (imagem) não funcionam: não há OCR.
- Documentos de exemplo fictícios (empresa "Vértice Logística").
- O observador de arquivos do Streamlit está desligado (`.streamlit/config.toml`);
  depois de editar o código, recarregue a página.

## Licença

Defina a licença antes de publicar (por exemplo, MIT).
