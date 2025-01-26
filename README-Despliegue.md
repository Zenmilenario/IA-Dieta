# Instrucciones de Despliegue 

### Requisitos previos

1. **Software necesario:**
   - Python 3.8 o superior.
   - Un sistema operativo que soporte Python (Windows, macOS, Linux).
2. **Bibliotecas requeridas:**
   - Flask
   - scikit-learn
   - pandas
   - joblib
   - numpy
   - matplotlib
3. **Archivo CSV con los datos nutricionales:**
   - Asegúrate de tener el archivo `Tabla_de_alimentos_ajustada.csv` en la carpeta principal del proyecto.

---

### Pasos para desplegar el proyecto

## Paso 1: Clonar el repositorio en tu IDE

1. Abre tu IDE preferido, como IntelliJ, Visual Studio Code o cualquier otro que soporte proyectos de Python.
2. Clona el repositorio desde GitHub directamente en el IDE:
   ```bash
   git clone https://github.com/zenmilenario/IA-Dieta.git
   
## Paso 2: Configurar el entorno del proyecto
El proyecto no requiere un entorno virtual específico. Asegúrate de que las bibliotecas necesarias están instaladas globalmente en tu sistema.

## Paso 3: Entrenar el modelo
Si necesitas generar el modelo desde cero, ejecuta el script `train_model.py`. Esto entrenará el modelo y generará un archivo llamado `modelo_ganador.pkl`:

1. Abre la terminal en tu IDE.
2. Ejecuta el siguiente comando:

   ```bash
   python train_model.py

## Paso 4: Iniciar el servidor Flask
Para iniciar la aplicación Flask, sigue estos pasos:

1. Abre la terminal en tu IDE.
2. Ejecuta el archivo `app.py` con el siguiente comando:
   ```bash
   python app.py
3. Por defecto, el servidor estará disponible en la siguiente URL:
   ```bash
   http://127.0.0.1:5000/

## Estructura del Proyecto
  El proyecto está organizado de la siguiente manera:
  
  ```plaintext
  |-- app.py                  # Archivo principal para iniciar la aplicación Flask
  |-- mi_modulo_dietas.py     # Módulo que contiene las funciones de generación de dietas
  |-- train_model.py          # Script para entrenar y guardar el modelo
  |-- templates/              # Archivos HTML para las vistas del prototipo
  |-- static/                 # Archivos estáticos como imágenes o CSS
  |-- Tabla_de_alimentos_ajustada.csv # Archivo de datos nutricionales
  |-- modelo_ganador.pkl      # Modelo preentrenado (se genera tras ejecutar train_model.py)
