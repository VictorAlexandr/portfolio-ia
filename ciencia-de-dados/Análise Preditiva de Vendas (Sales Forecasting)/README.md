# Análise Preditiva de Vendas (Sales Forecasting)

<img width="968" height="602" alt="image" src="https://github.com/user-attachments/assets/cab26999-6436-4941-98c3-1ea46036ddbb" />

## 1. Visão Geral do Projeto

Este projeto de ponta a ponta desenvolve um modelo de machine learning para prever tendências de vendas com base em dados históricos de transações. O objetivo é fornecer uma ferramenta para otimizar a gestão de estoque e o planejamento financeiro.

**[➡️ Acesse o Dashboard Interativo aqui](https://lookerstudio.google.com/reporting/83299bdc-370f-4a40-b985-a3f12aeb9a26)**

---

## 2. Stack de Tecnologias

*   **Linguagem de Programação:** Python
*   **Bibliotecas de Análise e Modelagem:** Pandas, Prophet (para forecasting), Scikit-learn (para métricas).
*   **Ambiente de Desenvolvimento:** Google Colab
*   **Ferramenta de Visualização (BI):** Google Looker Studio

---

## 3. Metodologia

O projeto seguiu as seguintes etapas:

1.  **Análise Exploratória de Dados (EDA):** Investigação dos dados para identificar tendências, sazonalidades e anomalias.
2.  **Pré-processamento:** Limpeza e transformação dos dados para o formato exigido pelo modelo Prophet.
3.  **Modelagem Preditiva:** Treinamento do modelo Prophet para aprender os padrões dos dados históricos.
4.  **Validação do Modelo:** Utilização de validação cruzada (cross-validation) para avaliar a performance do modelo com a métrica RMSE.
5.  **Visualização:** Criação de um dashboard interativo no Looker Studio para apresentar os resultados históricos, a previsão futura e os KPIs de negócio.

---

## 4. Principais Insights (Componentes do Modelo)

O modelo Prophet foi capaz de decompor a série temporal e revelar padrões importantes:
*   **Tendência de Crescimento:** O modelo confirmou uma forte tendência de crescimento nas vendas a partir de meados de 2015.
*   **Sazonalidade Semanal:** Foi identificado um pico claro de vendas aos sábados.
*   **Sazonalidade Anual:** Picos de vendas foram observados em meados do ano e um pico ainda maior no final do ano (Novembro/Dezembro).

---

## 5. Como Executar o Projeto

1.  Clone este repositório: `git clone https://github.com/seu-usuario/sales-forecasting-prophet.git`
2.  O notebook com todo o processo de análise e modelagem está na pasta `/notebooks`.
3.  O dataset utilizado pode ser encontrado no Kaggle: [Retail Sales Forecasting](https://www.kaggle.com/datasets/arlistle/retail-sales-forecasting).
