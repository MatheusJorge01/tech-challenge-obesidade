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
                                           
    st.markdown("---")
    if ("Prever"):
        # 1. Cria o dicionário com os valores das variáveis
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

        # 2. Transforma em DataFrame (O Pipeline cuidará do OneHotEncoding)
        input_data = pd.DataFrame([input_dict])

        # 3. Predição
        try:
            prediction = model.predict(input_data)[0]
            resultado = traducao_resultado.get(prediction, prediction)
            st.success(f"### Nível de obesidade previsto: {resultado}")
        except Exception as e:
            st.error(f"Erro ao processar predição: {e}")

# ==============================
# PÁGINA 2 — PAINEL ANALÍTICO
# ==============================
else:
    st.title(" Painel Analítico – Visão Médica Estratégica")

    # ==============================
    # Carregamento e preparação dos dados
    # ==============================
    try:
        df = pd.read_csv("Obesity.csv")
        df["BMI"] = df["Weight"] / (df["Height"] ** 2)
        df["Nivel_Obesidade"] = df["Obesity"].map(traducao_resultado)
    except Exception as e:
        st.error(f"Erro ao carregar a base de dados: {e}")
        st.stop()

    # ==============================
    # Abas
    # ==============================
    tab1, tab2 = st.tabs(
        [" Visão Geral e Insights", " Exploração Interativa"]
    )

    # ==============================
    # TAB 1 — VISÃO GERAL
    # ==============================
    with tab1:

        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total de Registros", len(df))
        c2.metric("IMC Médio", round(df["BMI"].mean(), 2))
        c3.metric("Idade Média", f"{round(df['Age'].mean(), 1)} anos")
        perc_hist = (df["family_history"] == "yes").mean() * 100
        c4.metric("Histórico Familiar (%)", f"{perc_hist:.1f}%")

        st.divider()

        # Distribuições principais
        st.subheader("Distribuição de Variáveis Físicas")

        g1, g2, g3 = st.columns(3)

        g1.plotly_chart(
            px.histogram(
                df,
                x="BMI",
                title="Distribuição do IMC",
                labels={
                    "BMI": "Índice de Massa Corporal (IMC)",
                    "count": "Quantidade de Indivíduos"
                }
            ),
            use_container_width=True
        )

        g2.plotly_chart(
            px.histogram(
                df,
                x="Age",
                title="Distribuição da Idade",
                labels={
                    "Age": "Idade (anos)",
                    "count": "Quantidade de Indivíduos"
                }
            ),
            use_container_width=True
        )

        g3.plotly_chart(
            px.histogram(
                df,
                x="CH2O",
                title="Distribuição do Consumo de Água",
                labels={
                    "CH2O": "Consumo Diário de Água (1=<1L | 2=1–2L | 3=>2L)",
                    "count": "Quantidade de Indivíduos"
                }
            ),
            use_container_width=True
        )

        st.subheader("Distribuição dos Níveis de Obesidade")

        st.plotly_chart(
            px.histogram(
                df,
                x="Nivel_Obesidade",
                color="Nivel_Obesidade",
                labels={
                    "Nivel_Obesidade": "Nível de Obesidade",
                    "count": "Quantidade de Indivíduos"
                }
            ),
            use_container_width=True
        )

        st.info(
            """
            **Insights Analíticos**
            - O IMC apresenta forte correlação com os níveis de obesidade.
            - A maior concentração da amostra está entre adultos jovens.
            - Indivíduos com histórico familiar positivo tendem a níveis mais elevados de obesidade.
            """
        )

    # ==============================
    # TAB 2 — EXPLORAÇÃO INTERATIVA
    # ==============================
    with tab2:

        st.subheader("Exploração Interativa dos Dados")

        nivel = st.multiselect(
            "Selecione os níveis de obesidade",
            df["Nivel_Obesidade"].unique(),
            df["Nivel_Obesidade"].unique()
        )

        idade_min, idade_max = st.slider(
            "Faixa etária",
            int(df["Age"].min()),
            int(df["Age"].max()),
            (18, 60)
        )

        df_filtrado = df[
            (df["Nivel_Obesidade"].isin(nivel)) &
            (df["Age"].between(idade_min, idade_max))
        ]

        st.plotly_chart(
            px.scatter(
                df_filtrado,
                x="Age",
                y="BMI",
                color="Nivel_Obesidade",
                labels={
                    "Age": "Idade (anos)",
                    "BMI": "IMC",
                    "Nivel_Obesidade": "Nível de Obesidade"
                },
                title="Relação entre Idade e IMC"
            ),
            use_container_width=True
        )


















