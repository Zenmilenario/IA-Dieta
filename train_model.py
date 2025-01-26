# train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

def train_and_save_model(
        csv_path="Tabla_de_alimentos_ajustada.csv",
        output_model_path="modelo_ganador.pkl"
):
    """
    Entrena dos modelos (RandomForest y LogisticRegression) sobre el CSV dado
    y guarda el mejor modelo en output_model_path.
    """
    df = pd.read_csv(csv_path)

    X = df[['calorias', 'proteinas', 'carbohidratos', 'grasas', 'fibra']]
    y = df['categoria']

    # Filtrar clases con menos de dos ejemplos
    clases_validas = y.value_counts()[y.value_counts() > 1].index
    df = df[df['categoria'].isin(clases_validas)]

    X = df[['calorias', 'proteinas', 'carbohidratos', 'grasas', 'fibra']]
    y = df['categoria']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Entrenar modelo Random Forest
    modelo1 = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )
    modelo1.fit(X_train, y_train)
    score1 = modelo1.score(X_test, y_test)

    # Entrenar modelo Logistic Regression
    modelo2 = make_pipeline(
        StandardScaler(),
        LogisticRegression(random_state=42, max_iter=1000)
    )
    modelo2.fit(X_train, y_train)
    score2 = modelo2.score(X_test, y_test)

    # Evaluar métricas de ambos modelos
    print("Evaluación de métricas:")
    print("\n--- Random Forest ---")
    y_pred_rf = modelo1.predict(X_test)
    print(classification_report(y_test, y_pred_rf))
    print("Matriz de confusión:")
    print(confusion_matrix(y_test, y_pred_rf))

    print("\n--- Logistic Regression ---")
    y_pred_lr = modelo2.predict(X_test)
    print(classification_report(y_test, y_pred_lr))
    print("Matriz de confusión:")
    print(confusion_matrix(y_test, y_pred_lr))

    # Elegir el modelo ganador
    if score1 >= score2:
        modelo_ganador = modelo1
        print(f"Modelo ganador: RandomForest (score={score1:.3f})")
    else:
        modelo_ganador = modelo2
        print(f"Modelo ganador: LogisticRegression (score={score2:.3f})")

    # Guardar el modelo ganador con joblib
    joblib.dump(modelo_ganador, output_model_path)
    print(f"Modelo guardado en: {output_model_path}")


if __name__ == "__main__":
    train_and_save_model()
