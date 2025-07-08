import streamlit as st
import json
import os

# CONFIG
HISTORY_FILE = 'history.json'
COLUMN_SIZE = 9

COLOR_MAP = {
    'R': {'name': 'Casa', 'color': '#EF4444', 'text': 'white'},
    'B': {'name': 'Visitante', 'color': '#3B82F6', 'text': 'white'},
    'Y': {'name': 'Empate', 'color': '#FACC15', 'text': 'black'}
}

# Funções de histórico
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(data):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f)

def split_columns(data):
    return [data[i:i+COLUMN_SIZE] for i in range(0, len(data), COLUMN_SIZE)]

def structurally_equal(col1, col2):
    if len(col1) != len(col2):
        return False
    pattern = {}
    for a, b in zip(col1, col2):
        if a in pattern:
            if pattern[a] != b:
                return False
        else:
            if b in pattern.values():
                return False
            pattern[a] = b
    return True

# Início da interface
st.set_page_config("Football Studio - Análise Padrões", layout="centered")
st.title("🎯 Análise de Padrões Estruturais (Football Studio)")
st.caption("Análise baseada em colunas de 9 com reescrita por estrutura")

if 'history' not in st.session_state:
    st.session_state.history = load_history()

# Botões de entrada
c1, c2, c3 = st.columns(3)
if c1.button("🔴 Casa"):
    st.session_state.history.append("R")
elif c2.button("🔵 Visitante"):
    st.session_state.history.append("B")
elif c3.button("🟡 Empate"):
    st.session_state.history.append("Y")

save_history(st.session_state.history)

# Mostrar colunas
columns = split_columns(st.session_state.history)
st.subheader("📊 Histórico em Colunas de 9")
col_layout = st.columns(len(columns))
for i, col_data in enumerate(columns):
    with col_layout[i]:
        st.markdown(f"**Col {i+1}**")
        for val in col_data:
            info = COLOR_MAP[val]
            st.markdown(
                f"<div style='background-color:{info['color']};color:{info['text']};text-align:center;padding:6px;border-radius:6px;margin:2px;font-weight:bold'>{val}</div>",
                unsafe_allow_html=True
            )

# Análise de repetição estrutural
st.markdown("---")
st.subheader("🤖 Sugestão Inteligente")

if len(columns) >= 4:
    nova = columns[-1]
    for i in range(len(columns)-1):
        antiga = columns[i]
        if structurally_equal(antiga, nova):
            st.success(f"🧠 Repetição detectada com Coluna {i+1} (estrutura compatível)")
            if i+1 < len(columns):
                prox_col = columns[i+1]
                if len(prox_col) > 0:
                    prox_val = prox_col[0]
                    cor = COLOR_MAP[prox_val]
                    st.markdown(
                        f"<div style='background-color:{cor['color']};color:{cor['text']};text-align:center;padding:10px;border-radius:6px;font-weight:bold'>🎯 Sugestão: {prox_val} ({cor['name']})</div>",
                        unsafe_allow_html=True
                    )
                    break
    else:
        st.info("Nenhuma repetição estrutural detectada ainda.")
else:
    st.warning("É necessário ao menos 4 colunas para análise.")

# Limpar
if st.button("🗑️ Limpar Histórico"):
    st.session_state.history = []
    save_history([])
    st.rerun()
