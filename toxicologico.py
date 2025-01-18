import streamlit as st
import pandas as pd

# Función para el criterio farmacológico
def calcular_farmacologico(area_utensilio):
    constante_1 = 395 / 1000
    constante_2 = 600000 / 4
    constante_3 = 1 / 491867.78
    limite_limpieza = constante_1 * constante_2 * constante_3 * area_utensilio
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    area_formateada = f"{area_utensilio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"Limite \\text{{de Limpieza}} = \\left(\\frac{{395 \\, \\text{{mg}}}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{600.000 \\, \\text{{und}}}}{{4 \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_formateada} \\, \\text{{cm}}^2}}{{491.867,78 \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado

# Función para el criterio PPM
def calcular_ppm(area_utensilio):
    constante_1 = 10
    constante_2 = 442.80
    constante_3 = 1 / 491867.78
    limite_limpieza = constante_1 * constante_2 * constante_3 * area_utensilio
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    area_formateada = f"{area_utensilio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"Limite \\text{{de Limpieza}} = \\left(\\frac{{10 \\, \\text{{mg}}}}{{\\text{{kg}}}} \\cdot 442,80 \\, \\text{{kg}}\\right) \\cdot "
        f"\\left(\\frac{{{area_formateada} \\, \\text{{cm}}^2}}{{491.867,78 \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado

# Función para el criterio toxicológico
def calcular_toxicologico(area_utensilio):
    constante_1 = 70
    constante_2 = (166 * 0.005) / 1000
    constante_3 = 600000 / 4
    constante_4 = 1 / 491867.78
    limite_limpieza = constante_1 * constante_2 * constante_3 * constante_4 * area_utensilio
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    area_formateada = f"{area_utensilio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"L'imite \\text{{de Limpieza}} = 70 \\, \\text{{kg}} \\cdot \\left(\\frac{{(166 \\, \\text{{mg/kg}} \\cdot 0,005)}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{600.000 \\, \\text{{und}}}}{{4 \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_formateada} \\, \\text{{cm}}^2}}{{491.867,78 \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado
#mar
def calcular_mar(area_utensilio):
    constante_1 = 0.00749
    constante_2 = 442800000
    constante_3 = 738
    constante_4 = 491867.78

    # Cálculo del límite de limpieza
    limite_limpieza = (constante_1 * constante_2 * area_utensilio) / (constante_3 * constante_4)

    # Formatear los valores con separadores de miles y decimales con ','
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    area_formateada = f"{area_utensilio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Construcción de la ecuación en formato LaTeX
    ecuacion = (
        f"MAR \\left( \\frac{{\\text{{mg}}}}{{\\text{{hisopo}}}} \\right) = "
        f"\\frac{{(0,00749 \\, \\text{{mg Detergente}} \\cdot 442.800.000 \\, \\text{{mg Albendazol}} \\cdot {area_formateada} \\, \\text{{cm}}^2)}}"
        f"{{738 \\, \\text{{mg Albendazol}} \\cdot 491.867,78 \\, \\text{{cm}}^2}} = {resultado} \\, \\text{{mg}}"
    )

    return ecuacion, resultado

# Configuración de la aplicación Streamlit
st.title("Límite de Limpieza")
st.write("Sube un archivo Excel con los datos y selecciona el criterio para calcular las ecuaciones.")

# Cargar el archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # Leer el archivo Excel
        data = pd.read_excel(uploaded_file)

        # Seleccionar criterio
        criterio = st.selectbox("Selecciona el criterio:", ["Farmacológico", "PPM", "Toxicológico", "MAR (mg/hisopo)"])

        # Procesar datos según el criterio
        ecuaciones = []
        if criterio == "Farmacológico":
            for area in data.iloc[:, 0]:
                ecuacion, resultado = calcular_farmacologico(area)
                ecuaciones.append({"Área": area, "Ecuación": ecuacion, "Resultado": resultado})
        elif criterio == "PPM":
            for area in data.iloc[:, 0]:
                ecuacion, resultado = calcular_ppm(area)
                ecuaciones.append({"Área": area, "Ecuación": ecuacion, "Resultado": resultado})
        elif criterio == "Toxicológico":
            for area in data.iloc[:, 0]:
                ecuacion, resultado = calcular_toxicologico(area)
                ecuaciones.append({"Área": area, "Ecuación": ecuacion, "Resultado": resultado})
        elif criterio == "MAR (mg/hisopo)":
            for area in data.iloc[:, 0]:
                ecuacion, resultado = calcular_mar(area)
                ecuaciones.append({"Área": area, "Ecuación": ecuacion, "Resultado": resultado})

        # Mostrar los resultados
        df_resultado = pd.DataFrame(ecuaciones)
        st.write(f"Resultados para el criterio {criterio}:")
        st.dataframe(df_resultado)

        # Descargar las ecuaciones generadas
        output_text = "\n".join([f"Área: {row['Área']}, {row['Ecuación']}" for _, row in df_resultado.iterrows()])
        st.download_button(
            label="Descargar ecuaciones generadas",
            data=output_text,
            file_name=f"ecuaciones_{criterio.lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")

