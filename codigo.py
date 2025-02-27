import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Calculadora de Bayes para COVID-19", layout="wide")

# Título y descripción
st.title("Calculadora de Teorema de Bayes para Pruebas de COVID-19")
st.markdown("""
Esta aplicación calcula la probabilidad posterior de tener COVID-19 dado un resultado positivo
en la prueba, utilizando el Teorema de Bayes.
""")

# Información del autor
st.sidebar.header("Desarrollado por:")
st.sidebar.markdown("""
**Nombre**: Carlos Andrés Rueda Ortega  
**Universidad**: UNAB (Universidad Autónoma de Bucaramanga)
""")

# Sidebar para parámetros de entrada
st.sidebar.header("Parámetros de entrada")

# Prevalencia (probabilidad previa)
prevalence = st.sidebar.slider(
    "Prevalencia (Probabilidad previa) P(A)",
    min_value=0.001,
    max_value=0.5,
    value=0.04,
    step=0.001,
    format="%.3f"
)

# Sensibilidad
sensitivity = st.sidebar.slider(
    "Sensibilidad P(B|A)",
    min_value=0.5,
    max_value=1.0,
    value=0.73,
    step=0.01,
    format="%.2f"
)

# Especificidad
specificity = st.sidebar.slider(
    "Especificidad P(¬B|¬A)",
    min_value=0.5,
    max_value=1.0,
    value=0.95,
    step=0.01,
    format="%.2f"
)

# Cálculo de la probabilidad posterior usando el Teorema de Bayes
# P(A|B) = P(B|A) * P(A) / P(B)
# donde P(B) = P(B|A) * P(A) + P(B|¬A) * P(¬A)

# Cálculo de la tasa de falsos positivos (1 - especificidad)
false_positive_rate = 1 - specificity

# Probabilidad de no tener COVID-19
prior_not_having_covid = 1 - prevalence

# Probabilidad total de dar positivo
total_probability_positive = (sensitivity * prevalence) + (false_positive_rate * prior_not_having_covid)

# Probabilidad posterior (tener COVID-19 dado un resultado positivo)
posterior_probability = (sensitivity * prevalence) / total_probability_positive

# Mostrar resultados
st.header("Resultados")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Probabilidad Posterior P(A|B)")
    st.markdown(f"""
    **Si obtienes un resultado positivo en la prueba de COVID-19:**
    
    La probabilidad de que realmente tengas COVID-19 es **{posterior_probability:.4f}** o **{posterior_probability * 100:.2f}%**
    """)

# Visualización
with col2:
    # Crear datos para el gráfico de barras
    labels = ['Probabilidad Previa', 'Probabilidad Posterior']
    values = [prevalence, posterior_probability]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=['blue', 'red'])
    
    # Añadir etiquetas de porcentaje
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.2%}', ha='center', va='bottom')
    
    ax.set_ylim(0, max(values) * 1.2)  # Ajustar el límite y para dejar espacio para las etiquetas
    ax.set_ylabel('Probabilidad')
    ax.set_title('Comparación de Probabilidad Previa vs. Posterior')
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

# Análisis de sensibilidad
st.header("Análisis de Sensibilidad")
st.markdown("""
Observa cómo cambia la probabilidad posterior cuando varías los parámetros:
* Si la **especificidad** es baja (es decir, alta tasa de falsos positivos), la probabilidad posterior P(A|B) 
  puede ser sorprendentemente baja, incluso con un resultado positivo.
* Si la **prevalencia** (probabilidad previa) es muy alta, un resultado positivo aumentará drásticamente 
  tu probabilidad posterior.
""")

# Definiciones
st.header("Definiciones")
st.markdown("""
**Prevalencia**: Porcentaje de la población que tiene COVID-19.

**Sensibilidad**: Probabilidad de que una prueba identifique correctamente a alguien con COVID-19.
Fórmula: Sensibilidad = Verdaderos Positivos / (Verdaderos Positivos + Falsos Negativos)

**Especificidad**: Probabilidad de que una prueba identifique correctamente a alguien sin COVID-19.
Fórmula: Especificidad = Verdaderos Negativos / (Verdaderos Negativos + Falsos Positivos)

**Probabilidad Posterior**: Probabilidad de tener COVID-19 dado un resultado positivo en la prueba.
""")

