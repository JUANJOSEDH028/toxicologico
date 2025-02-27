import streamlit as st
import pandas as pd

# Sección de entrada de datos manuales
st.title("Límite de Limpieza")

# Solicitar valores al usuario antes de cargar el archivo Excel
peso_tableta = st.number_input("Ingrese el peso de la tableta (mg)", min_value=0.0, format="%.2f")
tamano_lote = st.number_input("Ingrese el tamaño del lote (cantidad de tabletas)", min_value=0)
num_dosis = st.number_input("Ingrese el número de dosis", min_value=0)
area_total = st.number_input("Ingrese el área total del equipo (cm²)", min_value=0.0, format="%.2f")
tamano_lotekg = st.number_input("Ingrese el tamaño de lote en Kg", min_value=0.0, format="%.2f")
tamano_lotemg = st.number_input("Ingrese el tamanño de lote en mg", min_value=0.0, format="%.2f")
dl50 = st.number_input("Ingrese el Dl50", min_value=0, format="%.2f")
nombre_tableta = st.text_input("Ingrese el nombre del producto")

# Función para formatear números con coma decimal y punto para miles
def formato_es(numero):
    return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Función para el criterio farmacológico
def calcular_farmacologico(area_muestreo):
    if peso_tableta == 0 or tamano_lote == 0 or num_dosis == 0 or area_total == 0:
        return "Error: Falta ingresar datos", "N/A"

    constante_1 = peso_tableta / 1000
    constante_2 = tamano_lote / num_dosis
    constante_3 = 1 / area_total
    limite_limpieza = constante_1 * constante_2 * constante_3 * area_muestreo
    resultado = formato_es(limite_limpieza)
    
    # Formatear números para la ecuación
    # Peso tableta como número entero con separadores de miles
    peso_tableta_fmt = f"{int(peso_tableta):,}".replace(",", ".")
    # Tamaño de lote como número entero con separadores de miles
    tamano_lote_fmt = f"{tamano_lote:,}".replace(",", ".")
    area_muestreo_fmt = formato_es(area_muestreo)
    area_total_fmt = formato_es(area_total)
    
    ecuacion = (
        f" \\text{{Límite de Limpieza}} = \\left(\\frac{{{peso_tableta_fmt} \\, \\text{{mg}}}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{{tamano_lote_fmt} \\, \\text{{und}}}}{{{num_dosis} \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_muestreo_fmt} \\, \\text{{cm}}^2}}{{{area_total_fmt} \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
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
    resultado = formato_es(limite_limpieza)
    
    # Formatear números para la ecuación
    tamano_lotekg_fmt = formato_es(tamano_lotekg)
    area_muestreo_fmt = formato_es(area_muestreo)
    area_total_fmt = formato_es(area_total)
    
    ecuacion = (
        f" \\text{{Límite de Limpieza}} = \\left(\\frac{{10 \\, \\text{{mg}}}}{{\\text{{kg}}}} \\cdot {tamano_lotekg_fmt} \\, \\text{{kg}}\\right) \\cdot "
        f"\\left(\\frac{{{area_muestreo_fmt} \\, \\text{{cm}}^2}}{{{area_total_fmt} \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
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
    resultado = formato_es(limite_limpieza)
    
    # Formatear números para la ecuación
    # DL50 como número entero con separadores de miles
    dl50_fmt = f"{int(dl50):,}".replace(",", ".")
    # Tamaño de lote como número entero con separadores de miles
    tamano_lote_fmt = f"{tamano_lote:,}".replace(",", ".")
    area_muestreo_fmt = formato_es(area_muestreo)
    area_total_fmt = formato_es(area_total)
    
    ecuacion = (
        f"\\text{{Límite de Limpieza}} = 70 \\, \\text{{kg}} \\cdot \\left(\\frac{{({dl50_fmt} \\, \\text{{mg/kg}} \\cdot 0,005)}}{{1000}}\\right) \\cdot "
        f"\\left(\\frac{{{tamano_lote_fmt} \\, \\text{{und}}}}{{{num_dosis} \\, \\text{{und}}}}\\right) \\cdot "
        f"\\left(\\frac{{{area_muestreo_fmt} \\, \\text{{cm}}^2}}{{{area_total_fmt} \\, \\text{{cm}}^2}}\\right) = {resultado} \\, \\text{{mg}}"
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
    resultado = formato_es(limite_limpieza)
    
    # Formatear números para la ecuación
    # Tamaño de lote mg como número entero con separadores de miles
    tamano_lotemg_fmt = f"{int(tamano_lotemg):,}".replace(",", ".")
    # Peso tableta como número entero con separadores de miles
    peso_tableta_fmt = f"{int(peso_tableta):,}".replace(",", ".")
    area_muestreo_fmt = formato_es(area_muestreo)
    area_total_fmt = formato_es(area_total)
    
    ecuacion = (
        f"MAR \\left( \\frac{{\\text{{mg}}}}{{\\text{{hisopo}}}} \\right) = "
        f"\\frac{{(0,00749 \\, \\text{{mg Detergente}} \\cdot {tamano_lotemg_fmt} \\, \\text{{mg ({nombre_tableta})}} \\cdot {area_muestreo_fmt} \\, \\text{{cm}}^2)}}"
        f"{{{peso_tableta_fmt} \\, \\text{{mg ({nombre_tableta})}} \\cdot {area_total_fmt} \\, \\text{{cm}}^2}} = {resultado} \\, \\text{{mg}}"
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
            
            # Reemplazar \cdot por * en todas las ecuaciones
            ecuacion = ecuacion.replace("\\cdot", "*")
            
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
