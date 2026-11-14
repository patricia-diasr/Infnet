from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CAMINHO_CSV = Path("assinantes_neostream.csv")
COLUNAS_NUMERICAS = [
    "tempo_assinatura_meses",
    "uso_medio_semanal_horas",
    "numero_reclamacoes",
]
COLUNAS_CATEGORICAS = ["plano", "metodo_pagamento", "dispositivo_principal"]
COLUNAS_FEATURES = COLUNAS_NUMERICAS + COLUNAS_CATEGORICAS
GRADE_C = {"classificador__C": [0.01, 0.1, 1, 10, 100]}


def gerar_base():
    rng = np.random.default_rng(7)
    n = 12000

    plano = rng.choice(["basico", "padrao", "premium"], size = n, p = [0.4, 0.4, 0.2])
    metodo_pagamento = rng.choice(
        ["cartao_credito", "boleto", "pix"], size = n, p = [0.55, 0.20, 0.25]
    )
    dispositivo_principal = rng.choice(
        ["smart_tv", "celular", "computador", "tablet"],
        size = n,
        p = [0.35, 0.35, 0.20, 0.10],
    )
    tempo_assinatura_meses = np.round(
        np.clip(rng.exponential(scale = 14, size = n), 0, 72), 1
    )
    uso_medio_semanal_horas = np.round(np.clip(rng.normal(9, 4, n), 0, 40), 1)
    numero_reclamacoes = rng.poisson(0.4, n)

    logit_churn = (
        -0.85
        - 0.04 * tempo_assinatura_meses
        - 0.06 * uso_medio_semanal_horas
        + 0.5 * numero_reclamacoes
        + rng.normal(0, 0.6, n)
    )
    prob_churn = 1 / (1 + np.exp(-logit_churn))
    churn = (rng.uniform(0, 1, n) < prob_churn).astype(int)

    raio = np.sqrt(
        ((tempo_assinatura_meses - 40) / 20) ** 2
        + ((uso_medio_semanal_horas - 14) / 8) ** 2
    )
    ltv_alto = (raio < 1.0).astype(int)
    inverter = rng.random(n) < 0.05
    ltv_alto = np.where(inverter, 1 - ltv_alto, ltv_alto)

    return pd.DataFrame(
        {
            "cliente_id": [f"AST-{i:05d}" for i in range(1, n + 1)],
            "plano": plano,
            "metodo_pagamento": metodo_pagamento,
            "dispositivo_principal": dispositivo_principal,
            "tempo_assinatura_meses": tempo_assinatura_meses,
            "uso_medio_semanal_horas": uso_medio_semanal_horas,
            "numero_reclamacoes": numero_reclamacoes,
            "churn": churn,
            "ltv_alto": ltv_alto,
        }
    )


def carregar_base():
    if not CAMINHO_CSV.exists():
        gerar_base().to_csv(CAMINHO_CSV, index = False)
        print(f"Base {CAMINHO_CSV} gerada automaticamente.")
    return pd.read_csv(CAMINHO_CSV)


def treinar_pipeline(base):
    X, y = base[COLUNAS_FEATURES], base["churn"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, stratify = y, random_state = 42
    )

    preprocessador = ColumnTransformer(
        transformers = [
            ("numericas", StandardScaler(), COLUNAS_NUMERICAS),
            (
                "categoricas",
                OneHotEncoder(handle_unknown = "ignore"),
                COLUNAS_CATEGORICAS,
            ),
        ]
    )
    pipeline = Pipeline(
        steps = [
            ("preprocessamento", preprocessador),
            ("classificador", LogisticRegression()),
        ]
    )

    busca = GridSearchCV(pipeline, param_grid = GRADE_C, cv = 5, scoring = "roc_auc")
    busca.fit(X_train, y_train)

    pipeline_final = pipeline.set_params(**busca.best_params_).fit(X_train, y_train)
    return pipeline_final, busca, X_test, y_test

if __name__ == "__main__":
    pipeline_final, busca, X_test, y_test = treinar_pipeline(carregar_base())
    auc_teste = roc_auc_score(y_test, pipeline_final.predict_proba(X_test)[:, 1])

    print(f"Melhores hiperparâmetros: {busca.best_params_}")
    print(f"ROC AUC médio na validação cruzada: {busca.best_score_:.4f}")
    print(f"ROC AUC no teste: {auc_teste:.4f}")
