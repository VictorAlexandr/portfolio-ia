# Detecção de Fraudes em Transações com Isolation Forest

## Visão Geral do Projeto

Este projeto implementa um sistema de machine learning para a detecção de transações fraudulentas em cartões de crédito. Utilizando o dataset "Credit Card Fraud Detection" do Kaggle, o foco foi aplicar o algoritmo de detecção de anomalias **Isolation Forest** para identificar padrões suspeitos em um cenário de dados altamente desbalanceado.

O notebook `deteccao_de_fraudes.ipynb` contém todo o processo, desde a análise exploratória dos dados até a otimização de hiperparâmetros e o salvamento do modelo final.

---

## Resultados Chave

O principal desafio foi superar a limitação da alta acurácia (99.7%) do modelo inicial, que na prática detectava apenas **26%** das fraudes reais (baixo recall).

Através da otimização do hiperparâmetro `contamination`, foi possível encontrar um equilíbrio estratégico:

-   **Modelo Escolhido:** `contamination=0.01`
-   **Recall (Fraudes Detectadas):** **59%**
-   **Análise:** O modelo final mais do que dobra a capacidade de detecção de fraudes em comparação com o baseline, representando um ganho significativo para o negócio, mantendo os alertas falsos em um nível gerenciável.

---

## Stack de Tecnologias

-   **Linguagem:** Python 3
-   **Bibliotecas Principais:** Pandas, Scikit-learn, Matplotlib, Seaborn, Joblib
-   **Ambiente de Desenvolvimento:** Google Colab / Jupyter Notebook

---

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    cd nome-do-repositorio
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Baixe o Dataset:**
    Faça o download do dataset a partir do [Kaggle: Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) e coloque o arquivo `creditcard.csv` na raiz do projeto.

4.  **Execute o Notebook:**
    Abra e execute o notebook `deteccao_de_fraudes.ipynb` em um ambiente Jupyter.

---

## Estrutura dos Arquivos

```
.
├── deteccao_de_fraudes.ipynb   # Notebook principal com todo o desenvolvimento
├── isolation_forest_model.joblib # Modelo final treinado e salvo
├── creditcard.csv              # Dataset (deve ser baixado)
├── requirements.txt            # Lista de dependências do projeto
└── README.md                   # Este arquivo de documentação
```
