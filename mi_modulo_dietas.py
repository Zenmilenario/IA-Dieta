import os
import pandas as pd
import joblib
import random


file_name = os.environ.get("CSV_PATH", "Tabla_de_alimentos_ajustada.csv")
df_realistic = pd.read_csv(file_name)

# Convertir las columnas relevantes a valores numéricos
columnas_numericas = ['calorias', 'proteinas', 'carbohidratos', 'grasas', 'fibra']
for col in columnas_numericas:
    df_realistic[col] = pd.to_numeric(df_realistic[col], errors='coerce')

# Eliminar filas con valores faltantes en las columnas numéricas
df_realistic = df_realistic.dropna(subset=columnas_numericas)

# Imprimir información para verificar los datos después del ajuste
print("Datos ajustados del CSV:")
print(df_realistic.head())
print("Tipos de datos ajustados:")
print(df_realistic.dtypes)

# Cargar el modelo preentrenado en lugar de volver a entrenar
model_path = os.environ.get("MODEL_PATH", "modelo_ganador.pkl")
modelo_ganador = joblib.load(model_path)

# Restricciones
restricciones_predefinidas = {
    "celiaco": ["trigo", "cebada", "centeno", "pan", "pasta", "harina"],
    "vegano": ["carne", "pescado", "pollo", "huevo", "leche", "mantequilla", "queso", "miel","bacalao","cerdo", "cordero", "ternera", "merluza", "lomo","trucha","rabo","atun","pavo","salmón","solomillo","conejo","dorada","Filete","Albóndigas"],
    "vegetariano": ["carne", "pescado", "pollo","bacalao","cerdo"],
    "intolerante_a_lactosa": ["leche", "mantequilla", "queso", "yogur", "nata"]
}


def filtrar_por_categoria_modelo(df, modelo, categoria_objetivo):
    """
    Usa el modelo para predecir la categoría
    y selecciona las filas con la categoría objetivo.
    """
    try:
        # Seleccionar las columnas necesarias
        X_local = df[['calorias', 'proteinas', 'carbohidratos', 'grasas', 'fibra']]

        # Convertir a numérico y manejar valores faltantes
        X_local = X_local.apply(pd.to_numeric, errors='coerce')
        X_local = X_local.dropna()

        # Realizar predicciones
        predicciones = modelo.predict(X_local)

        # Agregar las predicciones al DataFrame y filtrar por categoría objetivo
        df_temp = df.copy()
        df_temp['categoria_predicha'] = predicciones
        return df_temp[df_temp['categoria_predicha'] == categoria_objetivo]

    except Exception as e:
        print(f"Error en filtrar_por_categoria_modelo: {e}")
        return pd.DataFrame()


def seleccionar_platos_op(candidatos, cal_obj, random_state, cal_tolerance=50, attempts=10):
    """
    Selecciona de 'candidatos' un subconjunto de alimentos que se acerque a 'cal_obj' calorías
    usando un metodo aleatorio con varios intentos.
    """
    best_diff = float('inf')
    best_combo = []

    for attempt in range(attempts):
        rs_attempt = random_state + attempt
        shuffled = candidatos.sample(frac=1, random_state=rs_attempt).reset_index(drop=True)

        total_cal = 0
        selected = []
        for _, alimento in shuffled.iterrows():
            if total_cal + alimento['calorias'] <= cal_obj:
                selected.append(alimento)
                total_cal += alimento['calorias']
            if total_cal >= cal_obj - cal_tolerance:
                break

        diff = abs(cal_obj - total_cal)
        if diff < best_diff:
            best_diff = diff
            best_combo = selected

    return pd.DataFrame(best_combo)

def construir_dieta(random_state, calorias_deseadas, predefinidas, adicionales=[]):
    """
    Construye una dieta con (Primero, Segundo, Postre) aplicando restricciones predefinidas y adicionales.
    """
    dieta_disponible = df_realistic.copy()

    # Filtrar por restricciones predefinidas
    for restriccion_predefinida in predefinidas:
        if restriccion_predefinida in restricciones_predefinidas:
            for palabra_clave in restricciones_predefinidas[restriccion_predefinida]:
                dieta_disponible = dieta_disponible[
                    ~dieta_disponible['alimento'].str.contains(
                        rf'\b{palabra_clave}\b', case=False, na=False
                    )
                ]

    # Filtrar por restricciones adicionales
    for palabra_clave in adicionales:
        dieta_disponible = dieta_disponible[
            ~dieta_disponible['alimento'].str.contains(
                rf'\b{palabra_clave}\b', case=False, na=False
            )
        ]

    print("Alimentos disponibles después de aplicar restricciones:")
    print(dieta_disponible[['alimento', 'categoria']])

    # Dividir calorías en 3 platos
    calorias_primero = int(calorias_deseadas * 0.30)
    calorias_segundo = int(calorias_deseadas * 0.50)
    calorias_postre  = int(calorias_deseadas * 0.20)

    categorias_obj = [
        ("Primero", calorias_primero),
        ("Segundo", calorias_segundo),
        ("Postre",  calorias_postre)
    ]

    partes = []
    for cat_str, cal_obj in categorias_obj:
        opciones_cat = filtrar_por_categoria_modelo(dieta_disponible, modelo_ganador, cat_str)
        print(f"Categoría: {cat_str}, Opciones disponibles: {len(opciones_cat)}")

        if len(opciones_cat) > 0:
            platos = seleccionar_platos_op(
                candidatos=opciones_cat,
                cal_obj=cal_obj,
                random_state=random_state,
                cal_tolerance=100,
                attempts=50
            )
            partes.append(platos)
        else:
            print(f"Advertencia: No hay suficientes opciones para la categoría '{cat_str}'.")
            partes.append(pd.DataFrame())  # Agregar un DataFrame vacío si no hay opciones

    return pd.concat(partes, ignore_index=True)

def generar_dietas_dobles(calorias_deseadas, predefinidas=[], adicionales=[], seed1=None, seed2=None):
    """
    Genera 2 dietas distintas con semillas diferentes
    """
    if seed1 is None:
        seed1 = random.randint(1, 100000)
    if seed2 is None:
        seed2 = random.randint(1, 100000)

    dieta_1 = construir_dieta(seed1, calorias_deseadas, predefinidas, adicionales)
    dieta_2 = construir_dieta(seed2, calorias_deseadas, predefinidas, adicionales)

    return {
        "Dieta 1": dieta_1,
        "Dieta 2": dieta_2
    }
