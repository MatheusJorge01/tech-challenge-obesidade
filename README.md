# Previsão do Nível de Obesidade

## Descrição do Projeto
Este projeto tem como objetivo desenvolver um modelo de Machine Learning capaz de prever o nível de obesidade de um indivíduo a partir de características físicas, hábitos alimentares e estilo de vida.

Além do modelo preditivo, foi desenvolvida uma aplicação interativa utilizando Streamlit, permitindo que usuários realizem previsões individuais e visualizem análises exploratórias dos dados.

## Problema de Negócio
A obesidade é um problema de saúde pública com impactos diretos na qualidade de vida e nos custos do sistema de saúde. A previsão do nível de obesidade pode auxiliar profissionais da área da saúde e gestores públicos na identificação de grupos de risco e na tomada de decisões preventivas.

## Dataset
O dataset utilizado contém informações como:
- Idade, altura e peso
- Hábitos alimentares
- Frequência de atividade física
- Consumo de álcool e tabaco
- Histórico familiar de obesidade

O arquivo utilizado é `Obesity.csv`.

## Modelo de Machine Learning
Foi utilizado um modelo de Random Forest Classifier, implementado dentro de um pipeline com pré-processamento de dados, incluindo:
- Codificação de variáveis categóricas
- Tratamento de variáveis numéricas

O modelo foi treinado para um problema de classificação multiclasse.

## Tecnologias Utilizadas
- Python
- Pandas
- Scikit-learn
- Joblib
- Streamlit
- Plotly

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

## Resultados e Avaliação do Modelo

O modelo de Machine Learning foi treinado utilizando um pipeline de pré-processamento e um classificador Random Forest.  
A avaliação foi realizada por meio de divisão entre conjunto de treino e conjunto de teste.

A acurácia obtida no conjunto de teste foi de **93,62%**, indicando uma boa capacidade do modelo em generalizar os padrões presentes nos dados e classificar corretamente os diferentes níveis de obesidade.

Os resultados demonstram que variáveis relacionadas a hábitos alimentares, nível de atividade física e índice de massa corporal (IMC) possuem forte influência na predição do nível de obesidade.
