# Tech Challenge – Previsão de Obesidade

## Descrição do Projeto
Este projeto tem como objetivo desenvolver uma solução de **Machine Learning** para **previsão do nível de obesidade** de indivíduos a partir de dados demográficos, comportamentais e de hábitos de vida.  

Além do modelo preditivo, foi construída uma **aplicação interativa em Streamlit**, permitindo tanto a **predição individual** quanto a **análise exploratória dos dados**, por meio de gráficos e indicadores analíticos.

O projeto faz parte do **Tech Challenge – Data Analytics** da FIAP.

---

## Dataset
O conjunto de dados utilizado é o **Obesity Dataset**, amplamente empregado em estudos de classificação de níveis de obesidade.

O dataset contém variáveis como:
- Idade  
- Altura  
- Peso  
- Gênero  
- Histórico familiar de obesidade  
- Hábitos alimentares  
- Consumo de água  
- Atividade física  
- Consumo de álcool  
- Meio de transporte  

A variável alvo representa os **níveis de obesidade**, categorizados em múltiplas classes.

---

## Modelo de Machine Learning
Foi utilizado um **Random Forest Classifier**, treinado dentro de um **pipeline de pré-processamento**, garantindo:
- Tratamento adequado de variáveis categóricas
- Padronização dos dados
- Reprodutibilidade do treinamento

### Avaliação
O modelo foi avaliado por meio da divisão entre **conjunto de treino e conjunto de teste**.

**Acurácia no conjunto de teste:**  
**✅ 93,62%**

Esse resultado indica boa capacidade de generalização e desempenho consistente na classificação dos níveis de obesidade.

---

## Aplicação Streamlit
A aplicação foi desenvolvida com **Streamlit** e está dividida em duas seções principais:

### Predição de Obesidade
- Formulário interativo para inserção dos dados do indivíduo
- Retorno do nível de obesidade previsto, apresentado em linguagem clara e amigável

### Painel Analítico
O painel analítico apresenta:
- Métricas gerais da base (IMC médio, idade média, consumo de água, etc.)
- Distribuição de indicadores (IMC, idade e consumo de água)
- Análise do perfil comportamental
- Distribuição percentual por gênero
- Visualizações por nível de obesidade
- Aba de **Exploração Interativa**, com filtros dinâmicos por idade e nível de obesidade

Essas visualizações permitem melhor compreensão dos padrões presentes nos dados e apoiam insights analíticos relevantes.

---

## Estrutura do Projeto

```text
tech_challenge_obesidade/
│
├── streamlit_app.py        # Aplicação Streamlit
├── train_model.py          # Script de treinamento do modelo
├── model_obesity.joblib    # Modelo treinado
├── Obesity.csv             # Dataset utilizado
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto
```

## Como Executar o Projeto

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate
```
### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Treinar o modelo
```bash
python train_model.py
```

### 4. Executar a aplicação
```bash
streamlit run streamlit_app.py
```

## Resultados, Avaliação do Modelo e Principais Insights

O modelo de Machine Learning foi desenvolvido utilizando um pipeline completo de pré-processamento, aliado a um classificador Random Forest, garantindo tratamento adequado das variáveis e maior robustez na etapa de treinamento.

A avaliação foi realizada por meio da divisão do conjunto de dados em treino e teste, permitindo mensurar a capacidade de generalização do modelo.

A acurácia obtida no conjunto de teste foi de 93,62%, indicando um desempenho consistente na classificação dos diferentes níveis de obesidade e boa aderência aos padrões presentes nos dados.

A análise dos resultados e do painel analítico permitiu identificar os seguintes principais insights:

O Índice de Massa Corporal (IMC) é o fator mais determinante na separação entre os níveis de obesidade, apresentando forte correlação com a variável alvo.

Adultos jovens concentram grande parte da amostra, indicando maior prevalência de variações nos níveis de obesidade nessa faixa etária.

Há uma associação significativa entre hábitos alimentares, especialmente o consumo de alimentos calóricos, e níveis mais elevados de obesidade.

A frequência de atividade física apresenta relação inversa com o grau de obesidade, reforçando seu papel como fator protetivo.

O histórico familiar de obesidade surge como um elemento relevante, sugerindo influência genética e comportamental.

Variáveis de estilo de vida, como consumo de água, tempo em dispositivos eletrônicos e consumo de álcool, contribuem para o contexto analítico e ajudam a explicar padrões observados no conjunto de dados.

De forma geral, os resultados demonstram que a combinação de fatores físicos, comportamentais e hábitos de vida é essencial para a predição eficaz do nível de obesidade, reforçando a importância de abordagens multidimensionais em problemas de saúde pública.
