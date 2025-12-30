import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# ==============================
# Configuração da página
# ==============================
st.set_page_config(
    page_title="Previsão de Obesidade",
    layout="wide"
)

# ==============================
# Dicionários de mapeamento (PT → Dataset)
# ==============================
map_genero = {
    "Feminino": "Female",
    "Masculino": "Male"
}

map_sim_nao = {
    "Sim": "yes",
    "Não": "no"
}

map_frequencia = {
    "Nunca": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

map_transporte = {
    "Carro": "Automobile",
    "Moto": "Motorbike",
    "Bicicleta": "Bike",
    "Transporte público": "Public_Transportation",
    "A pé": "Walking"
}

traducao_resultado = {
    "Insufficient_Weight": "Abaixo do peso",
    "Normal_Weight": "Peso normal",
    "Overweight_Level_I": "Sobrepeso – Nível I",
    "Overweight_Level_II": "Sobrepeso – Nível II",
    "Obesity_Type_I": "Obesidade – Grau I",
    "Obesity_Type_II": "Obesidade – Grau II",
    "Obesity_Type_III": "Obesidade – Grau III"
}

# ==============================
# Menu lateral
# ==============================
menu = st.sidebar.selectbox(
    "Menu",
    ["Predição de Obesidade", "Painel Analítico"]
)

# ==============================
# PÁGINA 1 — PREDIÇÃO
# ==============================
if menu == "Predição de Obesidade":

    st.title("Predição do Nível de Obesidade")
    st.write("Preencha os dados abaixo para obter a previsão.")

    model = joblib.load("model_obesity.joblib")

    col1, col2, col3 = st.columns(3)

    with col1:
        genero_pt = st.selectbox("Gênero", ["Feminino", "Masculino"])
        idade = st.number_input("Idade (anos)", min_value=14, max_value=61, value=30)
        altura = st.number_input("Altura (m)", min_value=1.40, max_value=2.00, value=1.70)
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
        historico_pt = st.selectbox("Histórico familiar de excesso de peso?", ["Sim", "Não"])

    with col2:
        favc_pt = st.selectbox("Consome alimentos muito calóricos?", ["Sim", "Não"])
        fcvc = st.selectbox(
            "Consumo de vegetais",
            [1, 2, 3],
            format_func=lambda x: {
                1: "Raramente",
                2: "Às vezes",
                3: "Sempre"
            }[x]
        )
        ncp = st.selectbox(
            "Número de refeições principais por dia",
            [1, 2, 3, 4],
            format_func=lambda x: {
                1: "Uma",
                2: "Duas",
                3: "Três",
                4: "Quatro ou mais"
            }[x]
        )
        caec_pt = st.selectbox(
            "Consumo de alimentos entre refeições",
            ["Nunca", "Às vezes", "Frequentemente", "Sempre"]
        )

    with col3:
        fuma_pt = st.selectbox("Fuma?", ["Sim", "Não"])
        ch2o = st.selectbox(
            "Consumo diário de água",
            [1, 2, 3],
            format_func=lambda x: {
                1: "Menos de 1 litro",
                2: "Entre 1 e 2 litros",
                3: "Mais de 2 litros"
            }[x]
        )
        scc_pt = st.selectbox("Monitora ingestão calórica?", ["Sim", "Não"])
        faf = st.selectbox(
            "Frequência de atividade física semanal",
            [0, 1, 2, 3],
            format_func=lambda x: {
                0: "Nenhuma",
                1: "1–2 vezes",
                2: "3–4 vezes",
                3: "5 vezes ou mais"
            }[x]
        )
        tue = st.selectbox(
            "Tempo diário em dispositivos eletrônicos",
            [0, 1, 2],
            format_func=lambda x: {
                0: "Até 2 horas",
                1: "3 a 5 horas",
                2: "Mais de 5 horas"
            }[x]
        )
        calc_pt = st.selectbox(
            "Consumo de bebida alcoólica",
            ["Nunca", "Às vezes", "Frequentemente", "Sempre"]
        )
        transporte_pt = st.selectbox(
            "Meio de transporte habitual",
            ["Carro", "Moto", "Bicicleta", "Transporte público", "A pé"]
        )

    if st.button("Prever"):
        input_data = pd.DataFrame([{
            "Gender": map_genero[genero_pt],
            "Age": idade,
            "Height": altura,
            "Weight": peso,
            "family_history": map_sim_nao[historico_pt],
            "FAVC": map_sim_nao[favc_pt],
            "FCVC": fcvc,
            "NCP": ncp,
            "CAEC": map_frequencia[caec_pt],
            "SMOKE": map_sim_nao[fuma_pt],
            "CH2O": ch2o,
            "SCC": map_sim_nao[scc_pt],
            "FAF": faf,
            "TUE": tue,
            "CALC": map_frequencia[calc_pt],
            "MTRANS": map_transporte[transporte_pt]
        }])

        prediction = model.predict(input_data)[0]
        resultado_final = traducao_resultado.get(prediction, prediction)

        st.success(f"Nível de obesidade previsto: {resultado_final}")

# ==============================
# PÁGINA 2 — PAINEL ANALÍTICO
# ==============================
else:

    st.title("Painel Analítico — Obesidade")

    df = pd.read_csv("Obesity.csv")

    # Calcular IMC
    df["BMI"] = df["Weight"] / (df["Height"] ** 2)

    # Traduzir níveis de obesidade
    df["Nivel_Obesidade"] = df["Obesity"].map(traducao_resultado)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            df,
            x="Nivel_Obesidade",
            title="Distribuição dos níveis de obesidade",
            labels={
                "Nivel_Obesidade": "Nível de obesidade",
                "count": "Quantidade"
            }
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            df,
            x="Age",
            y="BMI",
            color="Nivel_Obesidade",
            title="IMC por idade e nível de obesidade",
            labels={
                "Age": "Idade",
                "BMI": "IMC",
                "Nivel_Obesidade": "Nível de obesidade"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Principais insights observados")
    st.write(
        "- O IMC apresenta forte relação com os níveis de obesidade.\n"
        "- Adultos jovens concentram grande parte dos casos.\n"
        "- Hábitos alimentares e atividade física impactam diretamente a classificação."
    )









