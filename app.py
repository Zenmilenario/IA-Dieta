# app.py
from flask import Flask, request, render_template, flash
import os
from mi_modulo_dietas import generar_dietas_dobles

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generar_dieta", methods=["POST"])
def generar_dieta():
    calorias_str = request.form.get("calorias_deseadas", "2000")
    restricciones_str = request.form.get("restricciones", "")

    try:
        calorias = int(calorias_str)
        if calorias < 100 or calorias > 10000:
            raise ValueError
    except ValueError:
        flash("Calorías inválidas, usando valor por defecto (2000).", "warning")
        calorias = 2000

    restricciones = [r.strip().lower() for r in restricciones_str.split(",") if r.strip()]

    from random import randint
    random_seed_1 = randint(1, 100000)
    random_seed_2 = randint(1, 100000)

    # Llamamos a generar las dietas
    resultado = generar_dietas_dobles(calorias, restricciones)

    dieta_1_df = resultado["Dieta 1"]
    dieta_2_df = resultado["Dieta 2"]

    # Convertir a lista de dicts para mostrar en tabla
    dieta_1_list = dieta_1_df.to_dict(orient="records")
    dieta_2_list = dieta_2_df.to_dict(orient="records")

    # Calcular total de calorías para cada dieta
    total_cal_1 = dieta_1_df['calorias'].sum()
    total_cal_2 = dieta_2_df['calorias'].sum()

    # Calcular macronutrientes totales para cada dieta
    prot1 = dieta_1_df['proteinas'].sum()
    carbs1 = dieta_1_df['carbohidratos'].sum()
    fat1 = dieta_1_df['grasas'].sum()
    fib1 = dieta_1_df['fibra'].sum()

    prot2 = dieta_2_df['proteinas'].sum()
    carbs2 = dieta_2_df['carbohidratos'].sum()
    fat2 = dieta_2_df['grasas'].sum()
    fib2 = dieta_2_df['fibra'].sum()

    return render_template(
        "resultado.html",
        calorias=calorias,
        restricciones=restricciones,
        dieta_1=dieta_1_list,
        dieta_2=dieta_2_list,
        total_cal_1=total_cal_1,
        total_cal_2=total_cal_2,
        prot1=prot1, carbs1=carbs1, fat1=fat1, fib1=fib1,
        prot2=prot2, carbs2=carbs2, fat2=fat2, fib2=fib2
    )

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(port=5000, debug=debug_mode)
