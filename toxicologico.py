import streamlit as st
import pandas as pd

# Sección de entrada de datos manuales
st.title("Límite de Limpieza")

# Solicitar valores al usuario antes de cargar el archivo Excel
peso_tableta = st.number_input("Ingrese el peso de la tableta (mg)", min_value=0.0, format="%.2f")
tamano_lote = st.number_input("Ingrese el tamaño del lote (cantidad de tabletas)", min_value=0)
num_dosis = st.number_input("Ingrese el número de dosis", min_value=0)
area_total = st.number_input("Ingrese el área total del equipo (cm²)", min_value=0.0, format="%.2f")
tamano_lotekg=st.number_input("Ingrese el tamaño de lote en Kg", min_value=0.0, format="%.2f")
tamano_lotemg=st.number_input("Ingrese el tamanño de lote en mg", min_value=0.0, format="%.2f")
dl50=st.number_input("Ingrese el Dl50", min_value=0, format="%.2f")

# Función para el criterio farmacológico
def calcular_farmacologico(area_muestreo):
    if peso_tableta == 0 or tamano_lote == 0 or num_dosis == 0 or area_total == 0:
        return "Error: Falta ingresar datos", "N/A"

    constante_1 = peso_tableta / 1000
    constante_2 = tamano_lote / num_dosis
    constante_3 = 1 / area_total
    limite_limpieza = constante_1 * constante_2 * constante_3 * area_muestreo
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"L\\\\'imite \\text{{de Limpieza}} = \\left(\\frac{{{peso_tableta} \\, \\text{{mg}}}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{{tamano_lote} \\, \\text{{und}}}}{{{num_dosis} \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_muestreo} \\, \\text{{cm}}^2}}{{{area_total} \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado

# Función para el criterio PPM
def calcular_ppm(area_muestreo):
    if area_total == 0:
        return "Error: Falta ingresar datos", "N/A"

    constante_1 = 10
    constante_2 = tamano_lotekg
    constante_3 = 1 / area_total
    limite_limpieza = constante_1 * constante_2 * constante_3 * area_muestreo
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"L\\\\'imite \\text{{de Limpieza}} = \\left(\\frac{{10 \\, \\text{{mg}}}}{{\\text{{kg}}}} \\cdot 442,80 \\, \\text{{kg}}\\right) \\cdot "
        f"\\left(\\frac{{{area_muestreo} \\, \\text{{cm}}^2}}{{{area_total} \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado

# Función para el criterio toxicológico
def calcular_toxicologico(area_muestreo):
    if area_total == 0:
        return "Error: Falta ingresar datos", "N/A"

    constante_1 = 70
    constante_2 = (dl50 * 0.005) / 1000
    constante_3 = tamano_lote / num_dosis
    constante_4 = 1 / area_total
    limite_limpieza = constante_1 * constante_2 * constante_3 * constante_4 * area_muestreo
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"L\\\\'imite \\text{{de Limpieza}} = 70 \\, \\text{{kg}} \\cdot \\left(\\frac{{(166 \\, \\text{{mg/kg}} \\cdot 0,005)}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{600.000 \\, \\text{{und}}}}{{4 \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_muestreo} \\, \\text{{cm}}^2}}{{{area_total} \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado

# Función para el criterio MAR
def calcular_mar(area_muestreo):
    if area_total == 0:
        return "Error: Falta ingresar datos", "N/A"

    constante_1 = 0.00749
    constante_2 = tamano_lotemg
    constante_3 = peso_tableta
    constante_4 = area_total
    limite_limpieza = (constante_1 * constante_2 * area_muestreo) / (constante_3 * constante_4)
    resultado = f"{limite_limpieza:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ecuacion = (
        f"MAR \\left( \\frac{{\\text{{mg}}}}{{\\text{{hisopo}}}} \\right) = "
        f"\\frac{{(0,00749 \\, \\text{{mg Detergente}} \\cdot 442.800.000 \\, \\text{{mg Albendazol}} \\cdot {area_muestreo} \\, \\text{{cm}}^2)}}"
        f"{{738 \\, \\text{{mg Albendazol}} \\cdot {area_total} \\, \\text{{cm}}^2}} = {resultado} \\, \\text{{mg}}"
    )
    return ecuacion, resultado

# Subir archivo de Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel con las áreas de muestreo", type=["xlsx"])

if uploaded_file:
    try:
        # Leer el archivo Excel
        data = pd.read_excel(uploaded_file)

        # Seleccionar criterio
        criterio = st.selectbox("Selecciona el criterio:", ["Farmacológico", "PPM", "Toxicológico", "MAR (mg/hisopo)"])

        # Procesar datos según el criterio
        ecuaciones = []
        for area in data.iloc[:, 0]:
            if criterio == "Farmacológico":
                ecuacion, resultado = calcular_farmacologico(area)
            elif criterio == "PPM":
                ecuacion, resultado = calcular_ppm(area)
            elif criterio == "Toxicológico":
                ecuacion, resultado = calcular_toxicologico(area)
            elif criterio == "MAR (mg/hisopo)":
                ecuacion, resultado = calcular_mar(area)
            
            ecuaciones.append({"Área de Muestreo": area, "Ecuación": ecuacion, "Resultado": resultado})

        # Mostrar resultados
        df_resultado = pd.DataFrame(ecuaciones)
        st.write(f"Resultados para el criterio {criterio}:")
        st.dataframe(df_resultado)

        # Descargar ecuaciones generadas
        output_text = "\n".join([f"Área: {row['Área de Muestreo']}, {row['Ecuación']}" for _, row in df_resultado.iterrows()])
        st.download_button(
            label="Descargar ecuaciones generadas",
            data=output_text,
            file_name=f"ecuaciones_{criterio.lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
