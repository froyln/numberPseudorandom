import streamlit as st
import pandas as pd

def calcular_periodo_estimado(metodo, m):
    if m <= 0: return 0
    if metodo == "Mixto": return m
    if metodo == "Multiplicativo Binario": return m // 4
    if metodo == "Multiplicativo Decimal": return m // 20 if m >= 20 else "Variable"
    return "Desconocido"

st.set_page_config(page_title="Generadores Aleatorios", layout="wide")
st.title("Generadores de Números Pseudoaleatorios")

st.markdown("### Configuración del Generador")

metodo = st.selectbox("Método:", ["Mixto", "Multiplicativo Binario", "Multiplicativo Decimal"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    x0 = st.number_input("Semilla (X0):", value=7, step=1)
with col2:
    a = st.number_input("Multiplicador (a):", value=5, step=1)
with col3:
    es_mixto = (metodo == "Mixto")
    c = st.number_input("Incremento (c):", value=3 if es_mixto else 0, step=1, disabled=not es_mixto)
    if not es_mixto: c = 0 
with col4:
    m = st.number_input("Módulo (m):", value=16, min_value=1, step=1)

if st.button("Generar Tabla", type="primary"):
    vistos = set()
    resultados = []
    xn = x0
    falla = False
    iteracion_falla = -1
    
    for n in range(m + 1):
        if xn in vistos:
            falla = True
            iteracion_falla = n
            break
            
        vistos.add(xn)
        xn_mas_1 = (a * xn + c) % m
        
        if metodo == "Mixto":
            operacion_str = f"({a} * {xn} + {c}) mod {m}"
        else:
            operacion_str = f"({a} * {xn}) mod {m}"
            
        ri = xn / m
        
        resultados.append({
            "n": n,
            "Xn": xn,
            "Operación": operacion_str,
            "Xn+1": xn_mas_1,
            "ri": f"{ri:.5f}" 
        })
        
        xn = xn_mas_1

    st.markdown("### Tabla de Resultados")
    df = pd.DataFrame(resultados)
    
    st.dataframe(df, use_container_width=True, hide_index=True)

    periodo_estimado = calcular_periodo_estimado(metodo, m)
    periodo_real = len(resultados)
    
    st.markdown(f"**Periodo Estimado:** `{periodo_estimado}` | **Periodo Real Obtenido:** `{periodo_real}`")

    if falla:
        if periodo_estimado != "Variable" and periodo_real >= periodo_estimado:
            st.success(f"Éxito: Se alcanzó el periodo estimado ({periodo_estimado}). El ciclo se repite en n={iteracion_falla}.")
        else:
            st.error(f"Ciclo incompleto: El generador falló/repitió en n={iteracion_falla} con el valor Xn={xn}.")
    else:
        st.info("Se completó la generación hasta el módulo máximo sin repeticiones.")
