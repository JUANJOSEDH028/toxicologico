import streamlit as st
import pandas as pd

def calcular_limite_limpieza(area_utensilio):
    # Constantes de la ecuación
    constante_1 = 70  # 70 kg
    constante_2 = (166 * 0.005) / 1000  # (166 mg/kg * 0.005) / 1000
    constante_3 = 600000 / 4  # 600.000 und / 4 und
    constante_4 = 1 / 491867.78  # 1 / 491.867,78 cm²

    # Cálculo del límite de limpieza
    limite_limpieza = constante_1 * constante_2 * constante_3 * constante_4 * area_utensilio

    # Formatear los valores con separadores de miles y decimales con ','
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    area_formateada = f"{area_utensilio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Construcción de la ecuación en formato LaTeX
    ecuacion = (
        f"Limite \\text{{de Limpieza}} = 70 \\, \\text{{kg}} \\cdot \\left(\\frac{{(166 \\, \\text{{mg/kg}} \\cdot 0,005)}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{600.000 \\, \\text{{und}}}}{{4 \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_formateada} \\, \\text{{cm}}^2}}{{491.867,78 \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )

    return ecuacion, resultado

# Título de la aplicación
st.title("Aplicación de Límites Toxicológicos")
st.write("Sube un archivo Excel con los datos y genera las ecuaciones automáticamente.")

# Cargar el archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Leer el archivo Excel
        data = pd.read_excel(uploaded_file)

        # Verificar encabezados
        st.write("Encabezados del archivo:", data.columns)
        first_column = data.columns[0]  # Usar la primera columna

        ecuaciones = []

        # Procesar cada valor en la primera columna
        for area in data[first_column]:
            try:
                area_float = float(area)
                ecuacion, resultado = calcular_limite_limpieza(area_float)
                ecuaciones.append({"Área": area_float, "Ecuación": ecuacion})
            except ValueError:
                ecuaciones.append({"Área": area, "Ecuación": "Error: Valor no válido"})

        # Mostrar las ecuaciones generadas
        st.write("Ecuaciones generadas:")
        df_resultado = pd.DataFrame(ecuaciones)
        st.dataframe(df_resultado)

        # Crear archivo de texto con las ecuaciones
        output_text = "\n".join([eq["Ecuación"] for eq in ecuaciones])
        st.download_button(
            label="Descargar ecuaciones generadas",
            data=output_text,
            file_name="ecuaciones_resultado.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
