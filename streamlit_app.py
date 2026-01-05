import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

@st.cache_resource
def load_model():
    return joblib.load("model_obesity.joblib")

# ==============================
# Configuração da página
# ==============================
st.set_page_config(
    page_title="Previsão de Obesidade",
    layout="wide"
)

# ==============================
# Dicionários de mapeamento
# ==============================
map_genero = {"Feminino": "Female", "Masculino": "Male"}
map_sim_nao = {"Sim": "yes", "Não": "no"}
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
    "Insufficient_Weight": "Abaixo do Peso",
    "Normal_Weight": "Peso Normal",
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

    model = load_model()

    col1, col2, col3 = st.columns(3)

    with col1:
        genero_pt = st.selectbox("Gênero", ["Feminino", "Masculino"])
        idade = st.number_input("Idade (anos)", 14, 61, 30)
        altura = st.number_input("Altura (m)", 1.40, 2.00, 1.70)
        peso = st.number_input("Peso (kg)", 30.0, 200.0, 70.0)
        historico_pt = st.selectbox(
            "Histórico familiar de excesso de peso?",
            ["Sim", "Não"]
        )

    with col2:
        favc_pt = st.selectbox(
            "Consome alimentos muito calóricos?",
            ["Sim", "Não"]
        )

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
            "Consumo entre refeições",
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

        scc_pt = st.selectbox(
            "Monitora ingestão calórica?",
            ["Sim", "Não"]
        )

        faf = st.selectbox(
            "Atividade física semanal",
            [0, 1, 2, 3],
            format_func=lambda x: {
                0: "Nenhuma",
                1: "1–2 vezes",
                2: "3–4 vezes",
                3: "5 vezes ou mais"
            }[x]
        )

        tue = st.selectbox(
            "Tempo diário em telas",
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
            "Meio de transporte",
            list(map_transporte.keys())
        )
                                           
    if st.button("Prever"):
        input_dict = {
            "Gender": map_genero[genero_pt],
            "Age": idade,
            "Height": altura,
            "Weight": peso,
            "family_history": map_sim_nao[historico_pt],
            "FAVC": map_sim_nao[favc_pt],
            "FCVC": float(fcvc),
            "NCP": float(ncp),
            "CAEC": map_frequencia[caec_pt],
            "SMOKE": map_sim_nao[fuma_pt],
            "CH2O": float(ch2o),
            "SCC": map_sim_nao[scc_pt],
            "FAF": float(faf),
            "TUE": float(tue),
            "CALC": map_frequencia[calc_pt],
            "MTRANS": map_transporte[transporte_pt]
        }

        # SEGUNDO: Criamos o DataFrame que o modelo entende
        input_data = pd.DataFrame(
            [[input_dict[col] for col in model.feature_names_in_]],
            columns=model.feature_names_in_
        )

        # TERCEIRO: O modelo faz a previsão
        prediction = model.predict(input_data)[0]
        resultado = traducao_resultado.get(prediction, prediction)

        st.success(f"### Nível de obesidade previsto: {resultado}")

# ==============================
# PÁGINA 2 — PAINEL ANALÍTICO
# ==============================
else:

    st.title("Painel Analítico – Obesidade")

    df = pd.read_csv("Obesity.csv")
    df["BMI"] = df["Weight"] / (df["Height"] ** 2)
    df["Nivel_Obesidade"] = df["Obesity"].map(traducao_resultado)

    tab1, tab2 = st.tabs(["Visão Geral", "Exploração Interativa"])

    # ==============================
    # TAB 1 — VISÃO GERAL
    # ==============================
    with tab1:

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Indivíduos", len(df))
        col2.metric("IMC médio", round(df["BMI"].mean(), 2))
        col3.metric("Idade média", round(df["Age"].mean(), 1))
        col4.metric("Consumo médio de água", round(df["CH2O"].mean(), 1))

        st.subheader("Distribuição de Indicadores")

        g1, g2, g3 = st.columns(3)

        # IMC
        fig_imc = px.histogram(
            df,
            x="BMI",
            title="Distribuição do IMC",
            labels={"BMI": "Índice de Massa Corporal (IMC)"}
        )
        fig_imc.update_yaxes(title_text="Quantidade de Indivíduos")
        g1.plotly_chart(fig_imc, use_container_width=True)

        # Idade
        fig_idade = px.histogram(
            df,
            x="Age",
            title="Distribuição da Idade",
            labels={"Age": "Idade (Anos)"}
        )
        fig_idade.update_yaxes(title_text="Quantidade de Indivíduos")
        g2.plotly_chart(fig_idade, use_container_width=True)

        # Água
        fig_agua = px.histogram(
            df,
            x="CH2O",
            title="Distribuição do Consumo de Água",
            labels={
                "CH2O": "Consumo Diário de Água (Litros)"
            }
        )
        fig_agua.update_yaxes(title_text="Quantidade de Indivíduos")
        g3.plotly_chart(fig_agua, use_container_width=True)

        st.subheader("Distribuição dos Níveis de Obesidade")

        fig_ob = px.histogram(
            df,
            x="Nivel_Obesidade",
            color="Nivel_Obesidade",
            labels={"Nivel_Obesidade": "Nível de Obesidade"}
        )
        fig_ob.update_yaxes(title_text="Quantidade de Indivíduos")
        st.plotly_chart(fig_ob, use_container_width=True)

        fig_scatter = px.scatter(
            df,
            x="Age",
            y="BMI",
            color="Nivel_Obesidade",
            labels={
                "Age": "Idade (anos)",
                "BMI": "IMC"
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ==============================
    # TAB 2 — EXPLORAÇÃO INTERATIVA
    # ==============================
    with tab2:

        st.subheader("Exploração Interativa")

        nivel = st.multiselect(
            "Nível de obesidade",
            df["Nivel_Obesidade"].unique(),
            df["Nivel_Obesidade"].unique()
        )

        idade_min, idade_max = st.slider(
            "Faixa etária",
            int(df["Age"].min()),
            int(df["Age"].max()),
            (18, 60)
        )

        df_filtro = df[
            (df["Nivel_Obesidade"].isin(nivel)) &
            (df["Age"].between(idade_min, idade_max))
        ]

        fig_filtrado = px.scatter(
            df_filtro,
            x="Age",
            y="BMI",
            color="Nivel_Obesidade",
            labels={
                "Age": "Idade (anos)",
                "BMI": "IMC"
            }
        )

        st.plotly_chart(fig_filtrado, use_container_width=True)

    st.subheader("Principais Insights")
    st.write(
        "- O IMC é o principal fator de separação entre os níveis de obesidade.\n"
        "- Adultos jovens concentram grande parte da amostra.\n"
        "- Há forte associação entre hábitos alimentares, atividade física e obesidade.\n"
        "- O histórico familiar aparece como fator relevante."
    )















