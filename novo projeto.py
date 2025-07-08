import streamlit as st
import pandas as pd

# Função para carregar histórico
def load_history():
    return []

# Função para salvar histórico
def save_history(history):
    return history

# Função para analisar padrões
def analyze_patterns(history):
    patterns = []
    vermelho = 0
    azul = 0
    amarelo = 0
    for i in history:
        if i == "R":
            vermelho += 1
        elif i == "B":
            azul += 1
        elif i == "Y":
            amarelo += 1
    return vermelho, azul, amarelo

# Função para prever próximo resultado
def predict_next_result(history):
    vermelho, azul, amarelo = analyze_patterns(history)
    if vermelho > azul and vermelho > amarelo:
        return "B"
    elif azul > vermelho and azul > amarelo:
        return "R"
    elif amarelo > vermelho and amarelo > azul:
        return "R"
    else:
        if history[-1] == "R":
            return "B"
        elif history[-1] == "B":
            return "R"
        else:
            return "R"

# Interface
st.title("Football Studio - Análise de Padrões")
history = load_history()

# Entrada de resultados
st.header("Entrada de Resultados")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟥"):
        history.append("R")
        save_history(history)
with col2:
    if st.button("🟦"):
        history.append("B")
        save_history(history)
with col3:
    if st.button("🟨"):
        history.append("Y")
        save_history(history)

# Análise de padrões
st.header("Análise de Padrões")
if history:
    st.write("Histórico:", history)
    vermelho, azul, amarelo = analyze_patterns(history)
    st.write("Vermelho:", vermelho)
    st.write("Azul:", azul)
    st.write("Amarelo:", amarelo)
    next_result = predict_next_result(history)
    if next_result == "R":
        st.write("Próximo resultado:", "🟥")
    elif next_result == "B":
        st.write("Próximo resultado:", "🟦")
    else:
        st.write("Próximo resultado:", "🟨")

# Histórico
st.header("Histórico")
st.write(history)
