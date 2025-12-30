import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# 1. Carregar o dataset
# -----------------------------
print("Lendo dataset...")
df = pd.read_csv("Obesity.csv")

# -----------------------------
# 2. Separar variáveis explicativas e alvo
# -----------------------------
X = df.drop(columns=["Obesity"])
y = df["Obesity"]

# -----------------------------
# 3. Identificar colunas numéricas e categóricas
# -----------------------------
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()
numerical_features = X.select_dtypes(exclude=["object"]).columns.tolist()

# -----------------------------
# 4. Criar pré-processador
# -----------------------------
print("Criando pipeline de pré-processamento...")

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features),
    ]
)

# -----------------------------
# 5. Definir modelo
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# -----------------------------
# 6. Criar pipeline completo
# -----------------------------
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", model),
    ]
)

# -----------------------------
# 7. Separar treino e teste
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 8. Treinar modelo
# -----------------------------
print("Treinando modelo...")
pipeline.fit(X_train, y_train)

# -----------------------------
# 9. Avaliar modelo
# -----------------------------
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Acurácia no conjunto de teste: {accuracy:.2%}")

# -----------------------------
# 10. Salvar modelo treinado
# -----------------------------
joblib.dump(pipeline, "model_obesity.joblib")
print("Modelo treinado e salvo com sucesso.")




